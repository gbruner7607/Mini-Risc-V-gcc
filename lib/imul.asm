imul:
addi x2,x2,-48
sw x8,x2,44
addi x8,x2,48
sw x10,x8,-36
sw x11,x8,-40
lw x15,x8,-36
beq x15,x0,L2
lw x15,x8,-40
bne x15,x0,L3
L2:
addi x15,x0,0
jal x0,L4
L3:
sw x0,x8,-20
sw x0,x8,-24
jal x0,L5
L6:
lw x14,x8,-20
lw x15,x8,-36
add x15,x14,x15
sw x15,x8,-20
lw x15,x8,-24
addi x15,x15,1
sw x15,x8,-24
L5:
lw x14,x8,-24
lw x15,x8,-40
blt x14,x15,L6
lw x15,x8,-20
L4:
addi x10,x15,0
lw x8,x2,44
addi x2,x2,48
jalr x0,x1,0
