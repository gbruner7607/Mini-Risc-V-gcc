	.file	"add.c"
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
	.ident	"GCC: (GNU) 7.2.0"
