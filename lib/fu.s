	.file "fu.s"
fu:
	addi sp,sp,-32
	sw s0,28(sp)
	addi s0,sp,32
	sw a0,-20(s0)
	lw s0,28(sp)
	addi sp,sp,32	
	jr ra
