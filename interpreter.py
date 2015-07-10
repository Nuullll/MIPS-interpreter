# -*- coding: UTF-8 -*-
# interpreter.py

import sys

def num2bin(num_str, bits):
    if num_str.lower().startswith('0x'):
        return hex2bin(num_str[2:], bits)
    else:
        return dec2bin(num_str, bits)


def dec2bin(num_str, bits):
    '''convert decimal number to bin_str with n bits'''
    try:
        num = int(num_str)
    except ValueError:
        print('illegal decimal input:', num_str)
        raise

    if num >= 0:
        return ("{0:0%db}" % bits).format(num)
    else:
        return ("{0:0%db}" % bits).format(2**bits + num)


def hex2bin(num_str, bits):
    d = {'0':'0000', '1':'0001', '2':'0010', '3':'0011',
         '4':'0100', '5':'0101', '6':'0110', '7':'0111',
         '8':'1000', '9':'1001', 'a':'1010', 'b':'1011',
         'c':'1100', 'd':'1101', 'e':'1110', 'f':'1111'}
    bin_str = ''
    try:
        for ch in num_str:
            bin_str += d[ch.lower()]
    except KeyError:
        print('illegal hex input:', num_str)
        raise

    if len(bin_str) < bits:
        bin_str = bin_str[0] * (bits - len(bin_str)) + bin_str
    else:
        bin_str = bin_str[-bits:]

    return bin_str


def bin2hex(bin_str):
    '''convert binary num (word aligned) to hex num'''
    d = {'0000':'0', '0001':'1', '0010':'2', '0011':'3',
         '0100':'4', '0101':'5', '0110':'6', '0111':'7',
         '1000':'8', '1001':'9', '1010':'a', '1011':'b',
         '1100':'c', '1101':'d', '1110':'e', '1111':'f'}
    hex_str = ''
    word = ''
    for bit in bin_str:
        if len(word) < 3:
            word += bit
        else:
            word += bit
            hex_str += d[word]
            word = ''
    return '0x' + hex_str


def parseRegister(reg_str):
    '''e.g. reg_str = "$zero", will be parsed to "00000"'''
    regs = ['$zero', '$at', '$v0', '$v1', '$a0', '$a1', '$a2', '$a3',
            '$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7',
            '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7',
            '$t8', '$t9', '$k0', '$k1', '$gp', '$sp', '$fp', '$ra']
    try:
        return dec2bin(regs.index(reg_str), 5)
    except ValueError:
        print('undefined register:', reg_str)
        raise


def delComment(line_str):
    '''delete comments in a line'''
    line_str = line_str.replace(',', ', ')
    line_str = line_str.replace(':', ': ')
    try:
        return line_str[:line_str.index('#')].strip()
    except ValueError:
        return line_str.strip()


def parseLabel(non_comment_line):
    '''parse label and instruction'''
    if ':' in non_comment_line:
        return (True, non_comment_line[non_comment_line.index(':')+1:].strip())
    else:
        return (False, non_comment_line)


def parseInstruction(instruction, labels, cur_addr):
    '''parse instruction to bin_str'''
    l = instruction.split()
    op = l.pop(0)
    l = [item.rstrip(',') for item in l]
    if op in ['lw', 'sw']:
        return parseLwSw(op, l)
    elif op == 'lui':
        return parseLui(op, l)
    elif op in ['add', 'addu', 'sub', 'subu',
                'and', 'or', 'xor', 'nor',
                'slt', 'sltu']:
        return parseR(op, l)
    elif op in ['addi', 'addiu', 'andi', 'slti', 'sltiu']:
        return parseImm(op, l)
    elif op in ['sll', 'srl', 'sra']:
        return parseShift(op, l)
    elif op in ['beq', 'bne', 'blez', 'bgtz', 'bgez']:
        return parseBranch(op, l, labels, cur_addr)
    elif op in ['j', 'jal']:
        return parseJump(op, l, labels)
    elif op in ['jr', 'jalr']:
        return parseJumpReg(op, l)
    else:
        raise NameError('undefined instruction:', instruction)


def parseLwSw(op, argv):
    '''lw rt, offset(rs)
    sw rt, offset(rs)'''
    rt_str = parseRegister(argv[0])
    offset = argv[1][:argv[1].index('(')]
    rs = argv[1][argv[1].index('(')+1:argv[1].index(')')]
    opcode = num2bin('0x23', 6) if op == 'lw' else num2bin('0x2b', 6)
    return opcode + parseRegister(rs) + rt_str + num2bin(offset, 16)


def parseLui(op, argv):
    '''lui rt, imm'''
    return num2bin('0x0f', 6) + '0' * 5 + parseRegister(argv[0]) + num2bin(argv[1], 16)


def parseR(op, argv):
    '''R rd, rs, rt'''
    opcode = '0' * 6
    l = ['add', 'addu', 'sub', 'subu', 'and', 'or', 'xor', 'nor']
    funt = num2bin(str(int('0x20', 16) + l.index(op)), 6) if op in l else (num2bin('0x2a', 6)
            if op == 'slt' else num2bin('0x2b', 6))
    return (opcode + parseRegister(argv[1]) + parseRegister(argv[2])
            + parseRegister(argv[0]) + '0' * 5 + funt)


def parseImm(op, argv):
    '''Ri rt, rs, imm'''
    if op == 'addi':
        opcode = num2bin('0x08', 6)
    elif op == 'addiu':
        opcode = num2bin('0x09', 6)
    elif op == 'andi':
        opcode = num2bin('0x0c', 6)
    elif op == 'slti':
        opcode = num2bin('0x0a', 6)
    else:
        opcode = num2bin('0x0b', 6)

    return opcode + parseRegister(argv[1]) + parseRegister(argv[0]) + num2bin(argv[2], 16)


def parseShift(op, argv):
    '''shift rd, rt, shamt'''
    if op == 'sll':
        funt = '0' * 6
    elif op == 'srl':
        funt = num2bin('0x02', 6)
    else:
        funt = num2bin('0x03', 6)

    return '0' * 11 + parseRegister(argv[1]) + parseRegister(argv[0]) + num2bin(argv[2], 5) + funt


def parseBranch(op, argv, labels, cur_addr):
    '''branch rs, rt, label
    branchz rs, label'''
    offset_label = argv[-1]
    try:
        tar_addr = labels[offset_label]
    except KeyError:
        print('undefined label:', offset_label)
        raise

    offset = tar_addr - cur_addr - 1
    offset_str = num2bin(str(offset), 16)

    if op == 'beq':
        return '000100' + parseRegister(argv[0]) + parseRegister(argv[1]) + offset_str
    elif op == 'bne':
        return '000101' + parseRegister(argv[0]) + parseRegister(argv[1]) + offset_str
    elif op == 'blez':
        return '000110' + parseRegister(argv[0]) + '0' * 5 + offset_str
    elif op == 'bgtz':
        return '000111' + parseRegister(argv[0]) + '0' * 5 + offset_str
    elif op == 'bgez':
        return '000001' + parseRegister(argv[0]) + '00001' + offset_str
    else:
        raise NameError('unknown error')


def parseJump(op, argv, labels):
    '''jump label'''
    if op == 'j':
        return num2bin('0x02', 6) + num2bin(str(labels[argv[0]]), 26)
    else:
        return num2bin('0x03', 6) + num2bin(str(labels[argv[0]]), 26)


def parseJumpReg(op, argv):
    '''jr rs
    jalr rd, rs
    jalr rs'''
    if op == 'jr':
        return '0' * 6 + parseRegister(argv[0]) + '0' * 15 + num2bin('0x08', 6)
    else:
        rd_str = parseRegister(argv[0] if len(argv) == 2 else '$ra')
        return '0' * 6 + parseRegister(argv[-1]) + '0' * 5 + rd_str + '0' * 5 + num2bin('0x09', 6)


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as sfile:
        lines = [delComment(line) for line in sfile if delComment(line) != '']

    labels = {}
    instructions = []
    for line in lines:
        label, instruction = parseLabel(line)
        if label:
            labels[line[:-1]] = len(instructions)
            if instruction != '':
                instructions.append(instruction)
        else:
            instructions.append(instruction)

    with open('machinecode_bin.txt', 'w') as bin_out:
        with open('machinecode_hex.txt', 'w') as hex_out:
            for i in range(len(instructions)):
                bin_str = parseInstruction(instructions[i], labels, i)
                bin_out.write(bin_str + '\n')
                hex_out.write(bin2hex(bin_str) + '\n')

