xor x0,x0,x0
xor x2,x2,x2
xor x8,x8,x8
addi x2,x2,512
jal x1,main
jal x1,exit
main:
addi x2,x2,-32
sw x1,x2,28
sw x8,x2,24
addi x8,x2,32
addi x15,x0,16
sw x15,x8,-20
addi x15,x0,3
sw x15,x8,-24
lw x11,x8,-24
lw x10,x8,-20
jal x1,imod
sw x10,x8,-28
lw x12,x8,-28
lw x11,x8,-24
lw x10,x8,-20
jal x1,fu
modtest.L2:
jal x0,modtest.L2
imod:
addi x2,x2,-48
sw x8,x2,44
addi x8,x2,48
sw x10,x8,-36
sw x11,x8,-40
lw x15,x8,-36
sw x15,x8,-20
jal x0,imod.L2
imod.L3:
lw x14,x8,-20
lw x15,x8,-40
sub x15,x14,x15
sw x15,x8,-20
imod.L2:
lw x14,x8,-20
lw x15,x8,-40
sub x15,x14,x15
bge x15,x0,imod.L3
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
