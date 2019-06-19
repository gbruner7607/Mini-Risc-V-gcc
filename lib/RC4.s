	.file	"RC4.c"
	.option nopic
	.text
	.align	2
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-1072
	sw	ra,1068(sp)
	sw	s0,1064(sp)
	addi	s0,sp,1072
	sw	zero,-20(s0)
	j	.L2
.L3:
	lw	a5,-20(s0)
	slli	a5,a5,2
	addi	a4,s0,-16
	add	a5,a4,a5
	lw	a4,-20(s0)
	sw	a4,-1044(a5)
	lw	a5,-20(s0)
	addi	a5,a5,1
	sw	a5,-20(s0)
.L2:
	lw	a4,-20(s0)
	li	a5,255
	ble	a4,a5,.L3
	sw	zero,-32(s0)
	sw	zero,-24(s0)
	sw	zero,-28(s0)
	j	.L4
.L5:
	lw	a5,-28(s0)
	slli	a5,a5,2
	addi	a4,s0,-16
	add	a5,a4,a5
	lw	a4,-1044(a5)
	lw	a5,-32(s0)
	add	a4,a4,a5
	lw	a5,-24(s0)
	add	a5,a4,a5
	li	a1,256
	mv	a0,a5
	call	imod
	sw	a0,-24(s0)
	lw	a5,-28(s0)
	slli	a5,a5,2
	addi	a4,s0,-16
	add	a5,a4,a5
	lw	a5,-1044(a5)
	sw	a5,-36(s0)
	lw	a5,-24(s0)
	slli	a5,a5,2
	addi	a4,s0,-16
	add	a5,a4,a5
	lw	a4,-1044(a5)
	lw	a5,-28(s0)
	slli	a5,a5,2
	addi	a3,s0,-16
	add	a5,a3,a5
	sw	a4,-1044(a5)
	lw	a5,-24(s0)
	slli	a5,a5,2
	addi	a4,s0,-16
	add	a5,a4,a5
	lw	a4,-36(s0)
	sw	a4,-1044(a5)
	lw	a5,-28(s0)
	addi	a5,a5,1
	sw	a5,-28(s0)
.L4:
	lw	a4,-28(s0)
	li	a5,255
	ble	a4,a5,.L5
	lw	a5,-1060(s0)
	lw	a1,-1056(s0)
	lw	a2,-1052(s0)
	lw	a3,-1048(s0)
	lw	a4,-1044(s0)
	mv	a0,a5
	call	fu
.L6:
	j	.L6
	.size	main, .-main
	.ident	"GCC: (GNU) 7.2.0"
