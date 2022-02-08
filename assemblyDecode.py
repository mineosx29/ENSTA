import sys
import re

dic = {}
dic['STOP'] = 0x00
dic['ADD'] = 0x01
dic['SUB'] = 0x02
dic['MUL'] = 0x03
dic['DIV'] = 0x04
dic['AND'] = 0x05
dic['OR'] = 0x06
dic['XOR'] = 0x07
dic['SHL'] = 0x08
dic['SEQ'] = 0x0C
dic['LOAD'] = 0x0D
dic['STORE'] = 0x0E
dic['BRAZ'] = 0x0F
dic['BRANZ'] = 0x10
dic['JMP'] = 0x11


def decode(line, addr):
    if re.search('^#', line) or line == '\n':
        return None

    isLabel = False
    if re.search('\w+:', line):
        label = str(re.findall('\w+:', line)[0])
        label = label[:len(label)-1]
        dic[label] = addr
        isLabel = True

    if isLabel:
        opcode = re.findall('[a-zA-Z]+', line)[1]
    else:
        opcode = re.findall('[a-zA-Z]+', line)[0]
    print(opcode)

    val = 0x00
    opcode = opcode.upper()
    val += dic[opcode] << 27
    if opcode.upper() == 'STOP':
        return val
    
    elif re.search('(JMP)', opcode.upper()):

    elif re.search('(BRANZ | BRAZ)', opcode.upper()):

    elif re.search('(SCALL)', opcode.upper()):

    if isLabel:
        ass = re.findall('[rR]?-?\d+|\w+', line)[2:5]
    else:
        ass = re.findall('[rR]?-?\d+|\w+', line)[1:4]
    print(ass)

    if 'R' in ass[0].upper() and len(ass[0]) == 2:
        val += int(ass[0][1]) << 22
    else:
        val += int(dic[ass[0]]) << 22

    if 'R' in ass[1].upper():
        val += 1 << 21
        val += int(ass[1][1]) << 5
    else:
        val += 0 << 21
        val += int(ass[1]) << 5

    if 'R' in ass[2].upper() and len(ass[2]) == 2:
        val += int(ass[2][1])
    else:
        val += int(dic[ass[2]])

    print(hex(val))
    return val

FILE = DIRECTORY = sys.argv[1]

file = open(FILE, "r")
filename = "binaryCode.txt"
try:
    f = open(filename, 'x')
except:
    f = open(filename, 'w')

addr = 0

for l in file:
    try:
        bin = str('0x{:08x}'.format(decode(l, addr)))
        f.write(str('0x{:08x}'.format(addr) + ' '))
        f.write(bin + '\n')
        addr += 1
    except:
        pass
f.close()

# 1 - Donner un sens au travail
# 2 - Accessible / Confiance
# 3 - Travail Prescrit != Travail réel
# 4 - Sentiment d'appartenance
# 5 - Argent