#!/usr/bin/python3

import gccAssembler as asm 
import coe_assembler as coe
import gccPrep as prep 
import linker
# import sys 
import argparse
import re
import os

def makePath(filename):
	path = ""
	splt = filename.split('/')
	f = splt[-1] 
	if (len(splt) > 1):
		for i in range(len(splt) - 1):
			path += splt[i] + '/' 
	return path, f 

parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+', help='File Names (Takes .c and .s')
parser.add_argument('-c', '--coe', action='store_true', help='generate .coe file instead of .hex file')
parser.add_argument('-s', '--save_temps', action='store_true', help='save intermediate .s and .o files')
parser.add_argument('-o', '--output', type=str, default='a.hex')
args = parser.parse_args()


# if (len(sys.argv) == 1):
# 	print("USAGE: ./Mini-Risc-V-gcc <primary c file> <other optional c files> <optional assembly files>")
# 	exit()

# path, f = makePath(args.files[0])
# print(path)
# print(f)

paths = list()
files = list()

for f in args.files:
	ptmp, ftmp = makePath(f)
	paths.append(ptmp)
	files.append(ftmp)


# primaryfile = args.files[0]
# primaryfilebase = re.split('\.', primaryfile) 
# primaryfile = files[0]
# primaryfilebase = re.split('\.', primaryfile) 
# primarypath = path[0] 
# cmd = 'riscv32-unknown-elf-gcc -Ilib/ -S ' 
if (args.output == 'a.hex'):
	outpath = paths[0] 
	outfile = files[0].split('.')[0]
	if (args.coe):
		outfile += '.coe'
	else:
		outfile += '.hex'
else:
	outpath, outfile = makePath(args.output)

cmd1 = 'riscv32-unknown-elf-gcc -S '
cmd2 = 'riscv32-unknown-elf-as -o '
sfiles = list()
# ofiles = list()
# objname = args.output.split('.')[0] + '.o'
objname = outpath + outfile.split('.')[0] + '.o'
# print(len(sys.argv))


for i in range(len(files)):
	f = files[i]
	p = paths[i]
	fsplit = f.split('.')
	sfiles.append(outpath + fsplit[0] + '.s')
	if (fsplit[1] == 'c'):
		os.system(cmd1 + p + f + ' -o ' + outpath + fsplit[0] + '.s')




# for i in range(0, len(args.files)):
# 	# print(sys.argv[i])
# 	fsplit = re.split('\.', args.files[i])
# 	sf = fsplit[0] + '.s'
# 	# of = fsplit[0] + '.o'
# 	sfiles.append(sf)
# 	# ofiles.append(of)
# 	if (fsplit[1] == 'c'):
# 		# print('adding ' + sys.argv[i])
# 		cmd1 = cmd1 + args.files[i] + ' '
# # cmd = cmd + filenames

# os.system(cmd1)

cmd2 = cmd2 + objname + ' '

for i in range(len(sfiles)):
	cmd2 = cmd2 + ' ' + sfiles[i]

os.system(cmd2) 


# print(os.system('ls'))


linker.ld(objname, args.coe, outfile, outpath)


if not args.save_temps:
	os.system('rm ' + objname)
	for f in sfiles:
		os.system('rm ' + f)

