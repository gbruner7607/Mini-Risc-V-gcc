	.file	"printArray.c"
	.option nopic
	.text
	.align	2
	.globl	printArray
	.type	printArray, @function
printArray:
	addi	sp,sp,-48
	sw	s0,44(sp)
	addi	s0,sp,48
	sw	a0,-36(s0)
	sw	a1,-40(s0)
	sw	zero,-20(s0)
	j	.L2
.L3:
	lw	a5,-20(s0)
	slli	a5,a5,2
	lw	a4,-36(s0)
	add	a5,a4,a5
	lw	a5,0(a5)
	sw	a5,-24(s0)
	lw	a5,-20(s0)
	addi	a5,a5,1
	sw	a5,-20(s0)
.L2:
	lw	a4,-20(s0)
	lw	a5,-40(s0)
	blt	a4,a5,.L3
	nop
	lw	s0,44(sp)
	addi	sp,sp,48
	jr	ra
	.size	printArray, .-printArray
	.ident	"GCC: (GNU) 7.2.0"