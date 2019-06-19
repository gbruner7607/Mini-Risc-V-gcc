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
addi x15,x0,5
sw x15,x8,-20
lw x10,x8,-20
jal x1,fu
functest.L2:
jal x0,functest.L2
fu:
addi x2,x2,-32
sw x8,x2,28
addi x8,x2,32
sw x10,x8,-20
lw x11,x8,-20
addi x10,x10,2
lw x8,x2,28
addi x2,x2,32
jalr x0,x1,0
exit:
jal x1,exit
