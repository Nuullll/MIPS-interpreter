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
    try:
        return line_str[:line_str.index('#')].strip()
    except ValueError:
        return line_str.strip()


def isLabel(non_comment_line):
    '''return whether this line is a label'''
    return ':' in non_comment_line


def parseInstruction(instruction):
    '''parse instruction to bin_str'''
    l = instruction.split()
    op = l.pop(0)
    l = [item.rstrip(',') for item in l]
    if op in ['lw', 'sw']:
        return parseLwSw(op, l)


def parseLwSw(op, argv):
    '''lw rt, offset(rs)
    sw rt, offset(rs)'''
    rt_str = parseRegister(argv[0])
    offset = argv[1][:argv[1].index('(')]
    rs = argv[1][argv[1].index('(')+1:argv[1].index(')')]
    opcode = '100011' if op == 'lw' else '101011'
    return opcode + parseRegister(rs) + rt_str + num2bin(offset, 16)


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as sfile:
        lines = [delComment(line) for line in sfile if delComment(line) != '']

    labels = {}
    instructions = []
    for line in lines:
        if isLabel(line):
            labels[line[:-1]] = len(instructions)
        else:
            instructions.append(line)

    print(labels)
    print(instructions)
