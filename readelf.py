import binascii 
import pandas as pd
import sys

BYTE_ORDER = 'little'
sh_type_table = ['NULL', 'PROGBITS', 'SYMTAB', 'STRTAB', 'RELA', 'HASH', 'DYNAMIC', 'NOTE', 'NOBITS',
	'REL', 'SHLIB', 'DYNSYM', 'INIT_ARRAY', 'FINI_ARRAY', 'PREINIT_ARRAY', 'GROUP', 'SYMTAB_SHNDX', 'NUM']
sym_type_table = {0:'NOTYPE', 1:'OBJECT', 2:'FUNC', 3:'SECTION', 4:'FILE', 13:'LOPROC', 15:'HIPROC'}
sym_bind_table = {0:'LOCAL', 1:'GLOBAL', 2:'WEAK', 13:'LOPROC', 5:'HIPROC'}

#Section Header Entries
class SH_Entry:
	def __init__(self, elf, byteorder, shoff):
		# self.shoff = shoff
		self.int = lambda a : int.from_bytes(a, byteorder)
		self.name = ''
		self.name_offset = self.int(elf[0x00:0x04]) 
		self.type = sh_type_table[self.int(elf[0x04:0x08]) ]
		self.flags = self.int(elf[0x08:0x0c])
		self.addr = self.int(elf[0x0c:0x10]) 
		self.offset = self.int(elf[0x10:0x14])
		self.size = self.int(elf[0x14:0x18]) 
		self.link = self.int(elf[0x18:0x1c])
		self.info = self.int(elf[0x1c:0x20])
		self.addralign = self.int(elf[0x20:0x24])
		self.entsize = self.int(elf[0x24:0x28]) 

	def to_dict(self):
		return {
			# 'shoff' : self.shoff,
			'Name' : self.name,
			# 'Name Offset' : self.name_offset,
			'Type' : self.type ,
			'Flg' : hex(self.flags) ,
			'Addr' : hex(self.addr) ,
			'Off' : hex(self.offset) ,
			'Size' : hex(self.size) ,
			'Lk' : hex(self.link) ,
			'Inf' : hex(self.info) ,
			'Al' : hex(self.addralign),
			'ES' : hex(self.entsize),
		}

#Program bits section
#
class PROGBITS:
	def __init__(self, elf, header):
		self.int = header.int
		self.header = header
		self.elf = elf[header.offset:header.offset+header.size]
		self.data = list() 
		# self.hexdata = list() 
		for i in range(0, header.size, 4):
			word = self.elf[i:i+4]
			self.data.append(self.int(word))
			# self.hexdata.append(hex(self.int(word)))

	def pop(self, i):
		tmp = self.data.pop(i)
		return tmp

	# def insert(self, i, x):
	# 	self.data.insert(i, x):
		
	def __getitem__(self, arg):
		return self.data[arg] 

	def __repr__(self):
		retval = ''
		idx = 0
		for d in self.data:
			retval = retval + hex(idx) + "    " + "{0:#0{1}x}".format(d, 10) + '\n'
			idx += 4
		return retval

# String Table Section
# This contains null-terminated string information and associated indices. 
# There will always be at least one of these sections for the Section Header Table Names 
class STRTAB:
	def __init__(self, elf, header):
		self.header = header
		self.elf = elf[header.offset:header.offset+header.size] 
		self.data = {} 
		self.strtab = {}

		start = 0 
		nullterm = 0
		while(start < len(self.elf)):
			lastchar = self.elf[nullterm]
			while(lastchar != 0):
				nullterm = nullterm + 1
				lastchar = self.elf[nullterm]
			self.data[start] = self.elf[start:nullterm]
			self.strtab[start] = self.elf[start:nullterm].decode('ascii')
			nullterm = nullterm + 1
			start = nullterm

	def __getitem__(self, arg):
		return self.strtab[arg]

	def __repr__(self):
		retval = "index   string\n" 
		for i in self.strtab:
			retval = retval + "{:>5}".format(str(i)) + "   " + self.strtab[i] + "\n"
		return retval

#Entry to relocation table
class RELA_Entry:
		#RELA.info : bits 31:8 for symtable offset, bits 7:0 for rela_type
	def __init__(self, elf):
		rela_type_table = {0x1a:'R_RISCV-HI20', 0x1b:'R_RISCV_LO12_I', 51:'R_RISCV_RELAX', 
			0x12:'R_RISCV_CALL', 0x11:'R_RISCV_JAL', 0x10:'R_RISCV_BRANCH'}
		self.int = lambda a : int.from_bytes(a, BYTE_ORDER)
		self.offset = self.int(elf[0x00:0x04])
		self.info = self.int(elf[0x04:0x08])
		infostr = "{0:#0{1}x}".format(self.info, 10)
		self.type = rela_type_table[int(infostr[-2:], 16)]
		self.symtab_offset = int(infostr[2:-2], 16)
		self.sym_value = ''
		self.addend = self.int(elf[0x08:0x0c])


	def to_dict(self):
		return {
			'Offset' : "{0:#0{1}x}".format(self.offset, 10),
			'Info' : "{0:#0{1}x}".format(self.info, 10), 
			'Type' : self.type,
			'Symtab_Offset' : self.symtab_offset, 
			'Sym_Value' : self.sym_value,
			'Addend' : "{0:#0{1}x}".format(self.addend, 10),
		}

#Section Type Relocation Table
class RELA:
	def __init__(self, elf, header):
		self.int = header.int 
		self.header = header 
		self.elf = elf[header.offset:header.offset+header.size] 
		self.entries = list() 
		reloff = header.offset 
		size = header.size 
		end_sec = reloff + size
		entsize = header.entsize
		while(reloff < end_sec):
			subelf = elf[reloff:reloff+entsize]
			self.entries.append(RELA_Entry(subelf))
			reloff = reloff + entsize

	def __getitem__(self, arg):
		return self.entries[arg]

	def get_Sym_Values(self, symtab):
		for i in range(len(self.entries)):
			symtmp = symtab[self.entries[i].symtab_offset] 
			self.entries[i].sym_value = symtmp.value 

	def to_DataFrame(self):
		df = pd.DataFrame(columns = ['Offset', 'Info', 'Addend'])
		for ent in self.entries:
			df = df.append(ent.to_dict(), ignore_index=True)
		return df

#Entry to symbol table section
class SYMTAB_Entry:
	def __init__(self, elf):
		self.int = lambda a : int.from_bytes(a, BYTE_ORDER)
		self.name = ''
		self.name_offset = self.int(elf[0x00:0x04])
		self.value = self.int(elf[0x04:0x08])
		self.size = self.int(elf[0x08:0x0c])
		self.info = self.int(elf[0x0c:0x0d])
		self.type = sym_type_table[elf[0x0c] & 0x0f]
		self.bind = sym_bind_table[(elf[0x0c] >> 4) & 0x0f]
		self.other = self.int(elf[0x0d:0x0e])
		self.shndx = self.int(elf[0x0e:0x10])

	def to_dict(self):
		return {
			'Name' : self.name, 
			'Value' : hex(self.value),
			'Size' : hex(self.size), 
			'Info' : hex(self.info), 
			'Type' : self.type, 
			'Bind' : self.bind,
			'Other' : hex(self.other), 
			'Shndx' : hex(self.shndx),
		}

#Section type Sym Table
# Symbol Table holds information needed to locate and relocate a program's symbolic 
# definitions and references. 
class SYMTAB:
	def __init__(self, elf, header):
		self.int = header.int 
		self.header = header 
		self.elf = elf[header.offset:header.offset+header.size]
		self.entries = list() 
		symoff = header.offset 
		size = header.size
		end_sec = symoff + size 
		entsize = header.entsize
		while(symoff < end_sec):
			subelf = elf[symoff:symoff+entsize]
			self.entries.append(SYMTAB_Entry(subelf))
			symoff = symoff + entsize 

	def __getitem__(self, arg):
		return self.entries[arg]

	# Adds names to the symbol table using each entry's name_offset in the given string table
	def Entry_Names(self, strtab):
		for i in range(len(self.entries)):
			self.entries[i].name = strtab[self.entries[i].name_offset]

	def to_DataFrame(self):
		df = pd.DataFrame(columns = ['Name', 'Value', 'Size', 'Info', 'Type', 'Bind', 'Other', 'Shndx'])
		for ent in self.entries:
			df = df.append(ent.to_dict(), ignore_index=True)
		return df

# ELF Header segment of ELF file
class ELF_Header:
	def __init__(self, elf):
		#ELF Header
		self.elf = elf
		self.magic = int.from_bytes(elf[0x00:0x04], 'big')
		self.addrsize = elf[0x04]
		self.endianness = elf[0x05]
		if self.endianness == 0x1:
			self.byteorder = 'little'
			BYTE_ORDER = 'litle'
		else:
			self.byteorder = 'big'
			BYTE_ORDER = 'big'
		self.int = lambda a : int.from_bytes(a, self.byteorder)
		self.elf_version = elf[0x06]
		self.ABI = elf[0x07]
		self.ABI_version = elf[0x08]
		self.PAD = self.int(elf[0x09:0x10])
		self.type = self.int(elf[0x10:0x12])
		self.version = self.int(elf[0x14:0x18])
		self.entry = self.int(elf[0x18:0x1c])
		self.phoff = self.int(elf[0x1c:0x20])
		self.shoff = self.int(elf[0x20:0x24])
		# print(binascii.hexlify(elf[0x20:0x24]))
		self.flags = self.int(elf[0x24:0x28])
		self.ehsize = self.int(elf[0x28:0x2a])
		self.phentsize = self.int(elf[0x2a:0x2c])
		self.phnum = self.int(elf[0x2c:0x2e])
		self.shentsize = self.int(elf[0x2e:0x30])
		self.shnum = self.int(elf[0x30:0x32] )
		self.shstrndx = self.int(elf[0x32:0x34])



# ELF file contents
class ELF:
	def __init__(self, elf):
		self.elf = elf
		self.EH = ELF_Header(elf)

		shoff = self.EH.shoff 
		shoffbase = shoff
		shentsize = self.EH.shentsize
		shnum = self.EH.shnum
		byteorder = self.EH.byteorder
		self.SH = list() 
		for i in range(shnum):
			subelf = elf[shoff:shoff+shentsize]
			self.SH.append(SH_Entry(subelf, byteorder, shoff))
			shoff = shoff + shentsize
		self.Construct_Section_Names()
		self.SH_DF = pd.DataFrame(columns=['Name', 'Type', 'Addr', 'Off', 'Size', 'ES', 'Flg', 'Lk', 'Inf', 'Al']) 
		for ent in self.SH:
			self.SH_DF = self.SH_DF.append(ent.to_dict(), ignore_index=True)

		self.ConstructSections()

		# print("***shstrtab***")
		# print(self.sections['.shstrtab'])
		# # print(self.shstrtab)
		# print('\n***.data***')
		# print(self.sections['.data'])
		# if ('.sdata' in self.sections):
		# 	print('\n***.sdata***')
		# 	print(self.sections['.sdata'])
		# print('\n***.rela.text***')
		# print(self.sections['.rela.text'].to_DataFrame())
		# # print(self.rela.text.to_DataFrame())
		# print('\n***.text***')
		# print(self.sections['.text'])
		# print('\n***.symtab***')
		# print(self.sections['.symtab'].to_DataFrame())

	def Construct_Section_Names(self):
		shstrndx = self.EH.shstrndx 
		ent_shstrtab = self.SH[shstrndx]
		bin_shstrtab = self.elf[ent_shstrtab.offset:ent_shstrtab.offset+ent_shstrtab.size] 
		for i in range(len(self.SH)):
			name_offset = self.SH[i].name_offset 
			self.SH[i].name = self.ExtractName(bin_shstrtab, name_offset)


	def ExtractName(self, b, offset):
		start = offset 
		end = offset
		lastchar = b[end]
		while(lastchar != 0):
			end = end + 1 
			lastchar = b[end] 
		return b[start:end].decode('ascii')

	def ConstructSections(self):
		self.sections = {}
		fillnames = {}
		relatab = 'NORELATAB'
		for ent in self.SH:
			if ent.type == 'STRTAB':
				self.sections[ent.name] = STRTAB(self.elf, ent) 
			elif ent.type == 'SYMTAB':
				self.sections[ent.name] = SYMTAB(self.elf, ent) 
				fillnames[ent.name] = ent.link
			elif ent.type == 'RELA':
				self.sections[ent.name] = RELA(self.elf, ent) 
				relatab = ent.name
			elif ent.type == 'PROGBITS':
				self.sections[ent.name] = PROGBITS(self.elf, ent)

		for i in fillnames:
			self.sections[i].Entry_Names(self.sections[self.SH[fillnames[i]].name])

		if not(relatab == 'NORELATAB'):
			self.sections[relatab].get_Sym_Values(self.sections['.symtab'])

		self.sections['SH'] = self.SH
		# for i in self.sections:
		# 	secname = i[1:]
		# 	print(secname)
		# 	setattr(self, secname, self.sections[i])

		
	def SecIndex(self, name):
		for i in range(len(self.SH)):
			if (self.SH[i].name == name):
				return i 
		return -1 

	def keys(self):
		return self.sections.keys()

	def __getitem__(self, arg):
		return self.sections[arg]


# # with open('globaltest.o', 'rb') as f:
# with open(sys.argv[1], 'rb') as f:
# 	elf = bytearray(f.read())
		

# E = ELF(elf) 
# print(E.SH_DF)
# print(E['SH'][2].name)
