#!/usr/bin/python

import gccAssembler as asm 
import coe_assembler as coe
import gccPrep as prep 
# import sys 
import argparse
import re
import os

parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+', help='File Names (Takes .c and .s')
parser.add_argument('-c', '--coe', action='store_true', help='generate .coe file instead of hexfile')
args = parser.parse_args()


# if (len(sys.argv) == 1):
# 	print("USAGE: ./Mini-Risc-V-gcc <primary c file> <other optional c files> <optional assembly files>")
# 	exit()

# primaryfile = sys.argv[1]
primaryfile = args.files[0]
primaryfilebase = re.split('\.', primaryfile) 
cmd = 'riscv32-unknown-elf-gcc -Ilib/ -S ' 
filenames = list()
# print(len(sys.argv))
for i in range(0, len(args.files)):
	# print(sys.argv[i])
	fsplit = re.split('\.', args.files[i])
	newfile = fsplit[0] + '.s'
	filenames.append(newfile)
	if (fsplit[1] == 'c'):
		# print('adding ' + sys.argv[i])
		cmd = cmd + args.files[i] + ' '
# cmd = cmd + filenames

with open(primaryfile) as f:
	for line in f:
		line = line.strip('\n')
		if ('#include<' in line):
			# print("APPENDING")
			libfile = line.replace('#include<', '').replace('>','')
			fsplit = re.split('\.', libfile)
			sfile =fsplit[0] + '.s'
			if not (sfile in filenames):
				sfile = '/home/gray/Projects/Assembly/lib/' + sfile
				filenames.append(sfile)

# print(filenames)


os.system(cmd)
asmfile = prep.Prepare(filenames)
if (args.coe):
	coe.assemble(asmfile)
else:
	asm.assemble(asmfile)