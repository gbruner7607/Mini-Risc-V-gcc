print:
	addi sp,sp,-32
	sw s0,28(sp)
	addi s0,sp,32 
	li a1,1
	li a5,0
	lui a5,699050
	sw a0,8(a5)
	sw a1,4(a5)
	sw zero,4(a5)
	lw s0,28(sp)
	addi sp,sp,32
	jr ra		
