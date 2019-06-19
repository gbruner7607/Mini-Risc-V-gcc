import re 
# import sys 

def translateABI(reg):
	abi = {
		'zero':'x0',
		'ra':'x1',
		'sp':'x2',
		'gp':'x3',
		'tp':'x4',
		't0':'x5',
		't1':'x6',
		't2':'x7',
		's0':'x8',
		'fp':'x8',
		's1':'x9',
		'a0':'x10',
		'a1':'x11',
		'a2':'x12',
		'a3':'x13',
		'a4':'x14',
		'a5':'x15',
		'a6':'x16',
		'a7':'x17',
		's2':'x18',
		's3':'x19',
		's4':'x20',
		's5':'x21',
		's6':'x22',
		's7':'x23',
		's8':'x24',
		's9':'x25',
		's10':'x26',
		's11':'x27',
		't3':'x28',
		't4':'x29',
		't5':'x30',
		't6':'x31',
	}

	return abi.get(reg, "NONE")

skiplines = ['.file', '.option', '.text', '.align', '.globl', '.type', '.size', '.ident']

def construct(filename):
	outdata = list()
	with open(filename) as f:
		# skip = True
		for line in f:
			# print(line[0:5])
			line=line.strip('\n')
			# line = line.strip('\t')
			# print(line)
			# if (':' in line):
			# 	skip = False
			# if (skip) or ('.size' in line) or ('.ident' in line):
			# 	continue 
			skip = False
			for i in skiplines:
				if (i in line):
					skip=True
			if (skip):
				continue
			outline = ''
			if (':' in line):
				if ('.' in line):
					filename = filename.replace('/home/gray/Projects/Assembly/lib/', '')
					fsplit = re.split('\.', filename)
					outline = fsplit[0] + line
				else:
					outline = line
			else:
				ins = re.split(',|\(|\)|\\t| ', line)
				# print(ins)
				for i in range(len(ins)):
					if '.L' in ins[i]:
						filename = filename.replace('/home/gray/Projects/Assembly/lib/', '')
						fsplit = re.split('\.', filename)
						ins[i] = fsplit[0] + ins[i]
				if (ins[1] == 'j'):
					outline = 'jal x0,'+ins[2]
				elif (ins[1] == 'jalr' and len(ins) == 3):
					outline = 'jalr x1,' + ins[2] + ',0'
				elif (ins[1] == 'jr'):
					outline = 'jalr x0,'+translateABI(ins[2])+',0'
				elif ins[1] == 'li':
					outline = 'addi ' + translateABI(ins[2]) + ',x0,' + ins[3]
				elif ins[1] == 'mv': 
					outline = 'addi ' + translateABI(ins[2]) + ',' + translateABI(ins[3]) + ',0'
				elif ins[1] == 'ble':
					outline = 'bge ' + translateABI(ins[3]) + ',' + translateABI(ins[2]) + ',' + ins[4]
				elif ins[1] == 'call':
					outline = 'jal x1,' + ins[2]
				elif ins[1] == 'beqz':
					outline = 'beq ' + translateABI(ins[2]) + ',x0,' + ins[3]
				elif ins[1] == 'bnez':
					outline = 'bne ' + translateABI(ins[2]) + ',x0,' + ins[3]
				elif ins[1] == 'bgez':
					outline = 'bge ' + translateABI(ins[2]) + ',x0,' + ins[3]
				elif ins[1] == 'nop':
					outline = 'add x0,x0,x0'
				else:
					outline = outline + ins[1] + ' ' + translateABI(ins[2]) + ','
					# print(ins[3])
					rs1 = translateABI(ins[3])
					# print(rs1)
					if (rs1 == 'NONE'):
						outline = outline + translateABI(ins[4]) + ',' + ins[3]
					else:
						rs2 = translateABI(ins[4])
						if (rs2 == 'NONE'):
							# ins[4] = ins[4].strip('-')
							outline = outline + rs1 + ',' + ins[4]
						else:
							outline = outline + rs1 + ',' + rs2
			outdata.append(outline)
	return outdata

def writeToFile(filename, outdata):
	fsplit = re.split('\.', filename)
	outfile = fsplit[0] + '.asm'
	with open(outfile, 'w') as f:
		f.write('xor x2,x2,x2\n')
		f.write('xor x8,x8,x8\n')
		f.write('addi x2,x2,2048\n')
		f.write('jal x1,main\n')
		f.write('jal x1,exit\n')
		for line in outdata:
			# print(line)
			f.write(line + '\n')
		f.write('exit:\n')
		f.write('jal x1,exit\n')
	return outfile

def Prepare(filenames):
	outdata = list()
	for i in filenames:
		outdata = outdata + construct(i)
	filename = filenames[0]
	outfile = writeToFile(filename, outdata)
	return outfile 
# outdata = list()
# for i in range(1, len(sys.argv)):
# 	filename = sys.argv[i]
# 	outdata = outdata + construct(filename)

# filename = sys.argv[1]
# writeToFile(filename, outdata)
# filename = sys.argv[1]
# outdata = construct(filename)
# writeToFile(filename, outdata)