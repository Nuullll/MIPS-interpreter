# main.asm

    j       GCD             # reset
    j       Break           # break
    j       Exception       # exception

GCD:
    # $a0 = operand0, $a1 = operand1
    addi    $t0, $zero, 0   # t0 counts trailing zeros of operand0
    addi    $t1, $zero, 0   # t1 counts trailing zeros of operand1
    addi    $t2, $zero, 1   # t2 = 1

Loop1:
    and     $t3, $a0, $t2   # t3 = a0 & 1, if a0 is even then t3 = 0
    bne     $t3, $zero, Skip1   # jump to Skip1 if a0 is odd
    addi    $t0, $t0, 1     # t0 += 1
    srl     $a0, $a0, 1     # a0 /= 2
    j       Loop1

Skip1:
    

