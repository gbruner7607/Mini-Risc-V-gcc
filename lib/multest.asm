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
addi x15,x0,2
sw x15,x8,-20
addi x15,x0,6
sw x15,x8,-24
lw x11,x8,-24
lw x10,x8,-20
jal x1,imul
sw x10,x8,-28
multest.L2:
jal x0,multest.L2
imul:
addi x2,x2,-48
sw x8,x2,44
addi x8,x2,48
sw x10,x8,-36
sw x11,x8,-40
lw x15,x8,-36
beq a5,x0,imul.L2
lw x15,x8,-40
bne a5,x0,imul.L3
imul.L2:
addi x15,x0,0
jal x0,imul.L4
imul.L3:
sw x0,x8,-20
sw x0,x8,-24
jal x0,imul.L5
imul.L6:
lw x14,x8,-20
lw x15,x8,-36
add x15,x14,x15
sw x15,x8,-20
lw x15,x8,-24
addi x15,x15,1
sw x15,x8,-24
imul.L5:
lw x14,x8,-24
lw x15,x8,-40
blt x14,x15,imul.L6
lw x15,x8,-20
imul.L4:
addi x10,x15,0
lw x8,x2,44
addi x2,x2,48
jalr x0,x1,0
exit:
jal x1,exit
