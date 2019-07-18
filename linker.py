import readelf as re 
# import sys

class Object:
	def __init__(self, data, size, mem_base):
		self.base_addr = mem_base
		self.size = size / 4
		self.data = {} 
		pres_addr = self.base_addr
		i = 0
		for d in data:
			self.data[pres_addr] = d 
			pres_addr += 4
			i += 1
			if i >= self.size:
				break

	def __getitem__(self, arg):
		return self.data[arg]

	def get_addresses(self):
		return self.data.keys()

	def print(self):
		for i in self.data: 
			print(hex(i) + "    " + hex(self.data[i]))


class Linker:
	def __init__(self, filename):
		with open(filename, 'rb') as f:
			self.elf = bytearray(f.read())

		self.E = re.ELF(self.elf) 

		self.ins = list()
		self.ins.extend(self.E['.text'])
		# for i in self.ins:
		# 	print(hex(i))

	# Instantiates symbol table entries of type OBJECT. Generally these are global variables and arrays
	def CreateObjects(self):
		ObjectEntries = list()
		self.MemObjects = {}
		memdata = {}
		MEM_UPPER_LIMIT = 4096
		memsize = 0
		memlim = MEM_UPPER_LIMIT
		symtab = self.E['.symtab']
		idx = 0
		for entry in symtab:
			if (entry.type == 'OBJECT' ):#or (entry.type == 'NOTYPE' and entry.name != '')):
				ObjectEntries.append(idx)
				# print(entry.name)
				memsize += entry.size 
				# self.E['.symtab'][idx].value = memlim - memsize
			idx += 1

		# print(hex(memsize))

		membase = MEM_UPPER_LIMIT - memsize
		# print(hex(membase))
		presmem = membase
		for idx in ObjectEntries:
			self.E['.symtab'][idx].value = presmem
			entry = self.E['.symtab'][idx]
			shname = self.E['SH'][entry.shndx].name
			symname = entry.name 
			# print(shname)
			self.MemObjects[symname] = Object(self.E[shname], entry.size, presmem)
			# self.E['.symtab']
			presmem += entry.size


		# for i in self.MemObjects:
		# 	print(i)
		# 	self.MemObjects[i].print()

		# for i in range(len(self.E['.symtab'])):
		# 	if (self.E['.symtab'][i].type == 'OBJECT'):
		# 		ObjectEntries.append(self.E['.symtab'][i]) 
		# 		print(self.E['.symtab'][i].name)

	#Generates the instructions for loading global data into memory
	def CreateMemset(self):
		setaddr_opc = 0x513
		setval_opc = 0x593 
		store_opc = 0xb52023 
		self.memset = list()
		self.datamemsize = 0
		for objname in self.MemObjects:
			obj = self.MemObjects[objname]
			addresses = obj.get_addresses()
			# print("addresses")
			for addr in addresses:
				# print(addr)
				# print(obj[addr])
				self.memset.append(setaddr_opc | (addr << 20))
				self.memset.append(setval_opc | (obj[addr] << 20) )
				self.memset.append(store_opc)
				self.datamemsize += 4

		# print(self.memset)
		# for a in self.memset:
		# 	print(hex(a))

	#Creates the "start" of the program, by prepending instructions for setting the stack pointer,
	# loading necessary data into memory (created by CreateMemset function), and providing instructions
	# for jumping to main and exit
	def CreateStart(self):
		opcode = '1101111'
		rd = '00001'
		try:
			self.memset 
		except AttributeError:
			self.CreateMemset() 
		self.start = list()
		self.start.append(int('00214133', 16))
		self.start.append(int('20010113', 16))
		for m in self.memset:
			self.start.append(m) 
			# print(hex(m))
		rs1 = '00010'
		opc = '0010011'
		sp = 4096 - self.datamemsize
		# print(sp)
		imm = format(sp, '012b') + '00000' + '000' + rs1 + opc 
		# self.start.append(int(imm, 2))
		# print('jump to main')
		# print(len(self.start) - 1)
		# base = len(self.start)  - 1
		base = 0
		main_addr = 0
		#find address of main
		symtab = self.E['.symtab']
		for entry in symtab:
			if (entry.name == 'main'):
				main_addr = int(entry.value / 4)
				break 
		# print(hex(main_addr * 4))
		# print(main_addr)
		val = (main_addr + 1) - base 
		val = val*2 
		# print(val)
		if val<0:
			val=2**20+val 
		val_bin=format(val,'020b')
		ins_bin=val_bin[0]+val_bin[10:20]+val_bin[9]+val_bin[1:9]+rd+opcode
		self.start.append(int(ins_bin, 2))

		base = len(self.start)
		# base = 1;
		endbase = len(self.start) + len(self.E['.text'].data)
		val = endbase - base 
		val = val*2 
		if val<0:
			val=2**20+val 
		val_bin=format(val,'020b')
		ins_bin=val_bin[0]+val_bin[10:20]+val_bin[9]+val_bin[1:9]+rd+opcode
		self.start.append(int(ins_bin, 2))

	#Generates full hex data for the program
	def GenerateHex(self):
		self.ins = list() 
		try:
			self.start 
		except AttributeError:
			self.CreateStart() 
		for s in self.start:
			self.ins.append(s) 
		text = self.E['.text'].data 
		for t in text:
			self.ins.append(t) 
		self.ins.append(0xffdff0ef)

		# for h in self.ins:
		# 	print(hex(h))

		# print(len(self.ins))

	#Saves the hex instructions to a file
	def SaveHex(self, filename, coe = False):
		try:
			self.ins 
		except AttributeError:
			self.GenerateHex()
		f = open(filename, 'w')
		if (coe):
			f.write('memory_initialization_radix=16;\n'+'memory_initialization_vector=\n')
		for h in self.ins:
			hexstring = hex(h)[2:].zfill(8)
			# print(hexstring)
			f.write(hexstring + '\n')
		if (coe):
			f.write(';')
		f.close()

	def AdjustFuncOffsets(self, membase = 0x10):
		symtab = self.E['.symtab']
		idx = 0
		for entry in symtab:
			if (entry.type == 'FUNC'):
				self.E['.symtab'][idx].value += membase
				# print(entry.name)
			idx += 1

	#Updates values and addresses based on the relocation table 
	def RELA(self):
		text = self.E['.text'] 
		# print(text)
		relatext = self.E['.rela.text']
		symtab = self.E['.symtab']
		for entry in relatext:
			symtab_entry = symtab[entry.symtab_offset]
			if (entry.type == "R_RISCV_CALL"):
				offset = int(entry.offset / 4)
				# print(offset)
				# text.pop(offset)
				text.data[offset] = 0x00004033
				offset += 1
				jumpto = int(symtab_entry.value / 4)
				jumpfrom = offset 
				val = jumpto - jumpfrom -1
				val = val*2
				# print(jumpto)
				# print(jumpfrom)
				# print('offset for call ' + str(val))
				# print(hex(val))
				if val<0:
					val=2**20+val
				val_bin=format(val,'020b')
				opcode='1101111'
				rd = '00001'
				ins_bin=val_bin[0]+val_bin[10:20]+val_bin[9]+val_bin[1:9]+rd+opcode
				# print(ins_bin)
				# print(len(ins_bin))
				val_hex = format(int(ins_bin,2),'08x')
				# print(val_hex)
				# print(hex(ins))
				text.data[offset] = int(ins_bin, 2)
				# symtab[entry.symtab_offset].size = len(text.data)
			if (entry.type == 'R_RISCV_JAL'):
				offset = int(entry.offset / 4) 
				jumpto = int(symtab_entry.value / 4)
				jumpfrom = offset 
				val = jumpto - jumpfrom - 1
				val = val * 2

				if val < 0:
					val = 2**20+val 
				val_bin = format(val, '020b')
				opcode = '1101111'
				rd = '00000'
				ins_bin=val_bin[0]+val_bin[10:20]+val_bin[9]+val_bin[1:9]+rd+opcode
				val_hex = format(int(ins_bin, 2),'08x')
				text.data[offset] = int(ins_bin, 2)

			if (entry.type == 'R_RISCV_BRANCH'):
				print('RISCV_BRANCH')
				offset = int(entry.offset / 4) 
				jumpto = int(symtab_entry.value / 4)
				jumpfrom = offset 
				val = jumpto - jumpfrom - 1
				val = val * 2
				if val < 0:
					val = 2**12+ val
				imm = format(val, '012b')
				# print(imm)
				ins = format(text.data[offset], '032b')
				rs2=ins[7:12]
				# print(rs2)
				rs1=ins[12:17]
				# print(rs1)
				funct3=ins[17:20]
				# print(funct3)
				opcode=ins[25:32]
				# print(opcode)
				ins_bin=imm[0]+imm[2:8]+rs2+rs1+funct3+imm[8:]+imm[1]+opcode
				# print(format(int(ins_bin, 2),'08x'))
				text.data[offset] = int(ins_bin, 2)


			if (entry.type == "R_RISCV_LO12_I"):
				offset = int(entry.offset / 4)
				name = symtab_entry.name 
				# print('VAR NAME ' + name)
				addr = list(self.MemObjects[name].get_addresses())[0]
				# print('ADDR: ' + str(addr))
				# opcode = '0000011'
				data = text.data[offset] 
				data = data | (addr << 20)
				# print(hex(data))
				text.data[offset] = data

		# print(text)

		self.E.sections['.text'] = text
		self.E.sections['.symtab'] = symtab


def ld(filename, coe = False):
	L = Linker(filename)

	L.CreateObjects()
	L.CreateMemset()
	L.RELA()

	L.GenerateHex()


	splt = filename.split('.')
	outfile = splt[0] + '.hex'
# print(outfile)

	L.SaveHex(outfile, coe)


# E = re.ELF(sys.argv[1]) 
# print(E.SH_DF)
# print(E.sections['.symtab'].to_DataFrame())
# if ('.sdata' in E.sections):
# 	print('\n***.sdata***')
# 	print(E.sections['.sdata']) 
# if ('.data' in E.sections):
# 	print('\n***.data***')
# 	print(E.sections['.data'])