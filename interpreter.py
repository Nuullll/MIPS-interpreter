# -*- coding: UTF-8 -*-
# interpreter.py

def parseRegister(reg_str):
    '''e.g. reg_str = "$zero", will be parsed to "00000"'''
    regs = ['$zero', '$at', '$v0', '$v1', '$a0', '$a1', '$a2', '$a3',
            '$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7',
            '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7',
            '$t8', '$t9', '$k0', '$k1', '$gp', '$sp', '$fp', '$ra']
    try:
        bin_str = bin(regs.index(reg_str))[2:]
        bin_str = '0' * (5 - len(bin_str)) + bin_str
    except IndexError:
        print('undefined register:', reg_str)

    return bin_str

