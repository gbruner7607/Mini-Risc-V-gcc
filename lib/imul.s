	.file	"imul.c"
	.option nopic
	.text
	.align	2
	.globl	imul
	.type	imul, @function
imul:
	addi	sp,sp,-48
	sw	s0,44(sp)
	addi	s0,sp,48
	sw	a0,-36(s0)
	sw	a1,-40(s0)
	lw	a5,-36(s0)
	beqz	a5,.L2
	lw	a5,-40(s0)
	bnez	a5,.L3
.L2:
	li	a5,0
	j	.L4
.L3:
	sw	zero,-20(s0)
	sw	zero,-24(s0)
	j	.L5
.L6:
	lw	a4,-20(s0)
	lw	a5,-36(s0)
	add	a5,a4,a5
	sw	a5,-20(s0)
	lw	a5,-24(s0)
	addi	a5,a5,1
	sw	a5,-24(s0)
.L5:
	lw	a4,-24(s0)
	lw	a5,-40(s0)
	blt	a4,a5,.L6
	lw	a5,-20(s0)
.L4:
	mv	a0,a5
	lw	s0,44(sp)
	addi	sp,sp,48
	jr	ra
	.size	imul, .-imul
	.ident	"GCC: (GNU) 7.2.0"
