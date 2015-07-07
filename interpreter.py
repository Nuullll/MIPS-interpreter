# -*- coding: UTF-8 -*-
# interpreter.py

def dec2bin(num, bits):
    '''convert decimal number to bin_str with n bits'''
    if num >= 0:
        return ("{0:0%db}" % bits).format(num)
    else:
        return ("{0:0%db}" % bits).format(2**bits + num)


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


def delComment(line_str):
    '''delete comments in a line'''
    return line_str[:line_str.index('#')].strip()


