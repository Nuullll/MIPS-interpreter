# main.asm

    j       Reset           # reset
    j       Break           # break
    j       Exception       # exception

Reset:

    lui     $s2, 0x4000         # addr of timer: 0x40000000
    sw      $zero, 8($s2)       # TCON = 0
    lui     $t0, 0xffff
    addi    $t0, $t0, 0x3caf    # 0xffffffff - 0xffff3caf = 50000
    sw      $t0, 0($s2)         # TH = 0xffff3caf
    addi    $t0, $t0, 50000
    sw      $t0, 4($s2)         # TL = 0xffffffff
    addi    $t0, $zero, 3
    sw      $t0, 8($s2)         # TCON = 3


Break:
    lw      $t0, 8($s2)         # t0 = TCON
    andi    $t0, $t0, 0xfff9    # t0 &= 0xfffffff9
    sw      $t0, 8($s2)         # TCON = t0

    # $s0 = operand0, $s1 = operand1
    addi    $a0, $s0, 0
    addi    $a1, $s1, 0
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
    beq     $t0, $zero, Scan 
    sub     $t0, $t0, $t2   # t0 -= 1
    sll     $a0, $a0, 1     # a0 *= 2
    j       Loop4

Scan:
    lw      $t0, 20($s2)    # t0 = digi
    srl     $t1, $t0, 8     # t1 = {..., digi[11:8]}
    andi    $t1, $t1, 0x000f    # t1 = {0...0, digi[11:8]}
    sll     $t1, $t1, 1         # next digi
    addi    $t2, $zero, 0x0010  # t2 = {0...1, 0000}  fourth digi << 1
    bne     $t1, $t2, Display
    addi    $t1, $zero, 0x0001  # first digi
Display:
    addi    $t3, $zero, 0x0001  # first digi
    addi    $t4, $zero, 0x0002  # second digi
    addi    $t5, $zero, 0x0004  # third digi
    addi    $t6, $zero, 0x0008  # fourth digi
    beq     $t1, $t3, Digi1
    beq     $t1, $t4, Digi2
    beq     $t1, $t5, Digi3
    beq     $t1, $t6, Digi4
Digi1:
    

Exception:


    
