# main.asm

    j       GCD             # reset
    j       Break           # break
    j       Exception       # exception

GCD:
    # $a0 = operand0, $a1 = operand1
    addi    $a0, $zero, 132 
    addi    $a1, $zero, 66
    addi    $t0, $zero, 0   # t0 counts trailing zeros of operand0
    addi    $t1, $zero, 0   # t1 counts trailing zeros of operand1
    addi    $t2, $zero, 1   # t2 = 1

Loop1:
    and     $t3, $a0, $t2   # t3 = a0 & 1, if a0 is even then t3 = 0
    bne     $t3, $zero, Loop2   # jump to Loop2 if a0 is odd
    addi    $t0, $t0, 1     # t0 += 1
    srl     $a0, $a0, 1     # a0 /= 2
    j       Loop1

Loop2:
    and     $t3, $a1, $t2   # t3 = a1 & 1, if a1 is even then t3 = 0
    bne     $t3, $zero, Loop3    # jump to Loop3 if a1 is odd
    addi    $t1, $t1, 1     # t1 += 1
    srl     $a1, $a1, 1     # a1 /= 2
    j       Loop2

Loop3:
    beq     $a0, $a1, Skip
    sub     $t3, $a0, $a1   # t3 = a0 - a1
    bgtz    $t3, Positive   # jump to Positive if t3 > 0
    sub     $t3, $a1, $a0   # t3 = a1 - a0
    addi    $a1, $t3, 0     # a1 = t3
    j       Loop3
Positive:
    addi    $a0, $t3, 0     # a0 = t3
    j       Loop3

Skip:
    # goal: t0 = min(t0, t1)
    sub     $t3, $t1, $t0   # t3 = t1 - t0
    bgtz    $t3, Loop4
    addi    $t0, $t1, 0     # t0 = t1 if t1 <= t0
Loop4:
    # goal: a0 = a0 * 2**t0
    beq     $t0, $zero, Exit 
    sub     $t0, $t0, $t2   # t0 -= 1
    sll     $a0, $a0, 1     # a0 *= 2
    j       Loop4

Exit:
    addi    $v0, $a0, 0     # v0 = a0
    
    
Break:


Exception:


    
