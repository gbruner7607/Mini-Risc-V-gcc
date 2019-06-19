	.file	"test.c"
	.option nopic
	.text
	.align	2
	.globl	myadd
	.type	myadd, @function
myadd:
	addi	sp,sp,-32
	sw	s0,28(sp)
	addi	s0,sp,32
	sw	a0,-20(s0)
	sw	a1,-24(s0)
	lw	a4,-20(s0)
	lw	a5,-24(s0)
	add	a5,a4,a5
	mv	a0,a5
	lw	s0,28(sp)
	addi	sp,sp,32
	jr	ra
	.size	myadd, .-myadd
	.align	2
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-32
	sw	ra,28(sp)
	sw	s0,24(sp)
	addi	s0,sp,32
	li	a5,4
	sw	a5,-20(s0)
	li	a5,5
	sw	a5,-24(s0)
	lw	a1,-24(s0)
	lw	a0,-20(s0)
	call	myadd
	sw	a0,-28(s0)
.L4:
	j	.L4
	.size	main, .-main
	.ident	"GCC: (GNU) 7.2.0"
