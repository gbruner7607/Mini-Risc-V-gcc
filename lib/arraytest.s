	.file	"arraytest.c"
	.option nopic
	.text
	.align	2
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-80
	sw	ra,76(sp)
	sw	s0,72(sp)
	addi	s0,sp,80
	sw	zero,-20(s0)
	j	.L2
.L3:
	lw	a5,-20(s0)
	slli	a5,a5,2
	addi	a4,s0,-16
	add	a5,a4,a5
	lw	a4,-20(s0)
	sw	a4,-64(a5)
	lw	a5,-20(s0)
	addi	a5,a5,1
	sw	a5,-20(s0)
.L2:
	lw	a4,-20(s0)
	li	a5,9
	ble	a4,a5,.L3
	lw	a5,-68(s0)
	sw	a5,-24(s0)
	lw	a5,-64(s0)
	sw	a5,-28(s0)
	lw	a5,-60(s0)
	sw	a5,-32(s0)
	lw	a5,-56(s0)
	sw	a5,-36(s0)
	lw	a5,-52(s0)
	sw	a5,-40(s0)
	lw	a4,-40(s0)
	lw	a3,-36(s0)
	lw	a2,-32(s0)
	lw	a1,-28(s0)
	lw	a0,-24(s0)
	call	fu
.L4:
	j	.L4
	.size	main, .-main
	.ident	"GCC: (GNU) 7.2.0"
