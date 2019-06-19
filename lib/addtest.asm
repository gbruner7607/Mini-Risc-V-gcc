xor x0,x0,x0
xor x2,x2,x2
xor x8,x8,x8
addi x2,x2,100
jal x1,main
jal x1,exit
main:
addi x2,x2,-32
sw x1,x2,28
sw x8,x2,24
addi x8,x2,32
addi x15,x0,3
sw x15,x8,-20
addi x15,x0,4
sw x15,x8,-24
lw x11,x8,-24
lw x10,x8,-20
jal x1,myadd
sw x10,x8,-28
addtest.L2:
jal x0,addtest.L2
myadd:
addi x2,x2,-32
sw x8,x2,28
addi x8,x2,32
sw x10,x8,-20
sw x11,x8,-24
lw x14,x8,-20
lw x15,x8,-24
add x15,x14,x15
addi x10,x15,0
lw x8,x2,28
addi x2,x2,32
jalr x0,x1,0
exit:
jal x1,exit
