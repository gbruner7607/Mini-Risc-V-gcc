xor x0,x0,x0
xor x2,x2,x2
xor x8,x8,x8
addi x2,x2,512
jal x1,main
jal x1,exit
main:
addi x2,x2,-80
sw x1,x2,76
sw x8,x2,72
addi x8,x2,80
sw x0,x8,-20
jal x0,arraytest.L2
arraytest.L3:
lw x15,x8,-20
slli x15,x15,2
addi x14,x8,-16
add x15,x14,x15
lw x14,x8,-20
sw x14,x15,-64
lw x15,x8,-20
addi x15,x15,1
sw x15,x8,-20
arraytest.L2:
lw x14,x8,-20
addi x15,x0,9
bge x15,x14,arraytest.L3
lw x15,x8,-68
sw x15,x8,-24
lw x15,x8,-64
sw x15,x8,-28
lw x15,x8,-60
sw x15,x8,-32
lw x15,x8,-56
sw x15,x8,-36
lw x15,x8,-52
sw x15,x8,-40
lw x14,x8,-40
lw x13,x8,-36
lw x12,x8,-32
lw x11,x8,-28
lw x10,x8,-24
jal x1,fu
arraytest.L4:
jal x0,arraytest.L4
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
