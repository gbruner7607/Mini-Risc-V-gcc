	.file	"imod.c"
	.option nopic
	.text
	.align	2
	.globl	imod
	.type	imod, @function
imod:
	addi	sp,sp,-48
	sw	s0,44(sp)
	addi	s0,sp,48
	sw	a0,-36(s0)
	sw	a1,-40(s0)
	lw	a5,-36(s0)
	sw	a5,-20(s0)
	j	.L2
.L3:
	lw	a4,-20(s0)
	lw	a5,-40(s0)
	sub	a5,a4,a5
	sw	a5,-20(s0)
.L2:
	lw	a4,-20(s0)
	lw	a5,-40(s0)
	sub	a5,a4,a5
	bgez	a5,.L3
	lw	a5,-20(s0)
	mv	a0,a5
	lw	s0,44(sp)
	addi	sp,sp,48
	jr	ra
	.size	imod, .-imod
	.ident	"GCC: (GNU) 7.2.0"
