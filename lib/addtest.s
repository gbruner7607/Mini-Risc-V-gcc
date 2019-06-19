	.file	"addtest.c"
	.option nopic
	.text
	.align	2
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-32
	sw	ra,28(sp)
	sw	s0,24(sp)
	addi	s0,sp,32
	li	a5,3
	sw	a5,-20(s0)
	li	a5,4
	sw	a5,-24(s0)
	lw	a1,-24(s0)
	lw	a0,-20(s0)
	call	myadd
	sw	a0,-28(s0)
.L2:
	j	.L2
	.size	main, .-main
	.ident	"GCC: (GNU) 7.2.0"
