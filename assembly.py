import re
import sys


class Assembly:
    MNEMOMIC = ["stop", "add", "sub", "mul", "div", "and", "or", "xor","shl","shr","slt",
             "sle","seq","load","store","jmp","braz","branz","scall","stop"]

    dictionnaire_inst={}
    instruction = "[A-Z]{3}"
    reg = "[0-9]"

    fichier_asm = open(sys.argv[1], "r")
    data = fichier_asm.readlines()

    for n in range(0, len(MNEMOMIC)):
        dictionnaire_inst[MNEMOMIC[n]] = n + 1


    for d in data:
        liste = d.split(",")
        regex_inst = re.compile(instruction)
        registre = re.compile(reg)
