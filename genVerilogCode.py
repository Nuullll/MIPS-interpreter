# -*- coding: UTF-8 -*-
# genVerilogCode.py

def genCode(hex_input_file, instructions):
    '''gen InstructionMemory.v'''
    begin_str = '''
module InstructionMemory(Address, Instruction);
    input [31:0] Address;
    output reg [31:0] Instruction;

    always @(*)
        case (Address[9:2])
'''
    with open('InstructionMemory.v', 'w') as output:
        output.write(begin_str)
        indent = ' ' * 12
        with open(hex_input_file, 'r') as hex_input:
            i = 0
            for instruction in instructions:
                s = indent + '// ' + instruction + '\n'
                s += indent + '8\'d' + str(i) + ': '
                i += 1
                s += 'Instruction <= '
                hex_code = hex_input.readline()
                s += '32\'h' + hex_code[2:-1] + ';\n'
                output.write(s)
        output.write(indent + 'default: Instruction <= 32\'h00000000;\n')
        output.write(' ' * 8 + 'endcase\n')
        output.write('endmodule\n')

