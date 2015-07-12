# main.asm

    j       Reset           # reset
    j       Break           # break
    j       Exception       # exception

Reset:
    addi    $gp, $zero, 0       # gp = 0
    addi    $t0, $zero, 0x0040  # 0
    sw      $t0, 0($gp)
    addi    $t0, $zero, 0x0079  # 1
    sw      $t0, 4($gp)
    addi    $t0, $zero, 0x0024  # 2
    sw      $t0, 8($gp)
    addi    $t0, $zero, 0x0030  # 3
    sw      $t0, 12($gp)
    addi    $t0, $zero, 0x0019  # 4
    sw      $t0, 16($gp)
    addi    $t0, $zero, 0x0012  # 5
    sw      $t0, 20($gp)
    addi    $t0, $zero, 0x0002  # 6
    sw      $t0, 24($gp)
    addi    $t0, $zero, 0x0078  # 7
    sw      $t0, 28($gp)
    addi    $t0, $zero, 0x0000  # 8
    sw      $t0, 32($gp)
    addi    $t0, $zero, 0x0010  # 9
    sw      $t0, 36($gp)
    addi    $t0, $zero, 0x0008  # A
    sw      $t0, 40($gp)
    addi    $t0, $zero, 0x0003  # b
    sw      $t0, 44($gp)
    addi    $t0, $zero, 0x0046  # C
    sw      $t0, 48($gp)
    addi    $t0, $zero, 0x0021  # d
    sw      $t0, 52($gp)
    addi    $t0, $zero, 0x0006  # E
    sw      $t0, 56($gp)
    addi    $t0, $zero, 0x000e  # F
    sw      $t0, 60($gp)

    lui     $s2, 0x4000         # addr of timer: 0x40000000
    sw      $zero, 8($s2)       # TCON = 0
    addi    $t0, $zero, 0xffe6
    sw      $t0, 0($s2)         # TH = 0xffffffe6
    addi    $t0, $zero, 0xffff
    sw      $t0, 4($s2)         # TL = 0xffffffff
    addi    $t0, $zero, 3
    sw      $t0, 8($s2)         # TCON = 3
    
    addi    $t0, $zero, 0x00b4  # jump register: 45th instruction
    jr      $t0


Break:
    lw      $t0, 8($s2)         # t0 = TCON
    andi    $t0, $t0, 0xfff9    # t0 &= 0xfffffff9
    sw      $t0, 8($s2)         # TCON = t0

    # $s0 = operand0, $s1 = operand1
    addi    $a0, $s0, 0
    addi    $a1, $s1, 0
    beq     $a0, $zero, Scan    # return 0
    beq     $a1, $zero, Opr1zero    # a1 = 0
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

Opr1zero:
    addi    $a0, $zero, 0
Scan:
    addi    $v0, $a0, 0     # result: v0 = a0
    sw      $v0, 12($s2)    # led = v0

    lw      $t0, 20($s2)    # t0 = digi
    srl     $t1, $t0, 8     # t1 = {..., digi[11:8]}
    andi    $t1, $t1, 0x000f    # t1 = {0...0, digi[11:8]}
    sll     $t1, $t1, 1         # next digi
    addi    $t2, $zero, 0x0010  # t2 = {0...1, 0000}  fourth digi << 1
    bne     $t1, $t2, Select
    addi    $t1, $zero, 0x0001  # first digi
Select:
    addi    $t3, $zero, 0x0001  # first digi
    addi    $t4, $zero, 0x0002  # second digi
    addi    $t5, $zero, 0x0004  # third digi
    addi    $t6, $zero, 0x0008  # fourth digi
    beq     $t1, $t3, Digi1
    beq     $t1, $t4, Digi2
    beq     $t1, $t5, Digi3
    beq     $t1, $t6, Digi4
    addi    $t1, $zero, 0x0001  # initial
Digi1:
    srl     $t2, $s0, 4
    j       Display
Digi2:
    andi    $t2, $s0, 0x000f
    j       Display
Digi3:
    srl     $t2, $s1, 4
    j       Display
Digi4:
    andi    $t2, $s1, 0x000f
    j       Display
Display:
    sll     $t2, $t2, 2
    add     $t3, $gp, $t2
    lw      $t2, 0($t3)
    sll     $t1, $t1, 8
    add     $t0, $t1, $t2       # t0 = digi[11:0]
    sw      $t0, 20($s2)        # digi = t0

    lw      $t0, 8($s2)         # t0 = TCON
    addi    $t1, $zero, 0x0002
    or      $t0, $t0, $t1       # t0 |= 0x00000002
    sw      $t0, 8($s2)         # TCON = t0

    jr      $k0                 # jump to $26

Exception:
    jr      $k1                 # jump to $27
