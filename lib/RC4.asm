xor x0,x0,x0
xor x2,x2,x2
xor x8,x8,x8
addi x2,x2,2048
jal x1,main
jal x1,exit
main:
addi x2,x2,-1072
sw x1,x2,1068
sw x8,x2,1064
addi x8,x2,1072
sw x0,x8,-20
jal x0,RC4.L2
RC4.L3:
lw x15,x8,-20
slli x15,x15,2
addi x14,x8,-16
add x15,x14,x15
lw x14,x8,-20
sw x14,x15,-1044
lw x15,x8,-20
addi x15,x15,1
sw x15,x8,-20
RC4.L2:
lw x14,x8,-20
addi x15,x0,255
bge x15,x14,RC4.L3
sw x0,x8,-32
sw x0,x8,-24
sw x0,x8,-28
jal x0,RC4.L4
RC4.L5:
lw x15,x8,-28
slli x15,x15,2
addi x14,x8,-16
add x15,x14,x15
lw x14,x15,-1044
lw x15,x8,-32
add x14,x14,x15
lw x15,x8,-24
add x15,x14,x15
addi x11,x0,256
addi x10,x15,0
jal x1,imod
sw x10,x8,-24
lw x15,x8,-28
slli x15,x15,2
addi x14,x8,-16
add x15,x14,x15
lw x15,x15,-1044
sw x15,x8,-36
lw x15,x8,-24
slli x15,x15,2
addi x14,x8,-16
add x15,x14,x15
lw x14,x15,-1044
lw x15,x8,-28
slli x15,x15,2
addi x13,x8,-16
add x15,x13,x15
sw x14,x15,-1044
lw x15,x8,-24
slli x15,x15,2
addi x14,x8,-16
add x15,x14,x15
lw x14,x8,-36
sw x14,x15,-1044
lw x15,x8,-28
addi x15,x15,1
sw x15,x8,-28
RC4.L4:
lw x14,x8,-28
addi x15,x0,255
bge x15,x14,RC4.L5
lw x15,x8,-1060
lw x11,x8,-1056
lw x12,x8,-1052
lw x13,x8,-1048
lw x14,x8,-1044
addi x10,x15,0
jal x1,fu
RC4.L6:
jal x0,RC4.L6
imod:
addi x2,x2,-48
sw x8,x2,44
addi x8,x2,48
sw x10,x8,-36
sw x11,x8,-40
lw x15,x8,-36
sw x15,x8,-20
jal x0,/home/gray/Projects/Assembly/lib/imod.L2
/home/gray/Projects/Assembly/lib/imod.L3:
lw x14,x8,-20
lw x15,x8,-40
sub x15,x14,x15
sw x15,x8,-20
/home/gray/Projects/Assembly/lib/imod.L2:
lw x14,x8,-20
lw x15,x8,-40
sub x15,x14,x15
bge x15,x0,/home/gray/Projects/Assembly/lib/imod.L3
lw x15,x8,-20
addi x10,x15,0
lw x8,x2,44
addi x2,x2,48
jalr x0,x1,0
fu:
addi x2,x2,-32
sw x8,x2,28
addi x8,x2,32
sw x10,x8,-20
lw x8,x2,28
addi x2,x2,32
jalr x0,x1,0
exit:
jal x1,exit
