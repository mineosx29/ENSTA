# Fichier python permettant de assembler.
import re
import sys
fichier = open(sys.argv[1], "r")
donnee = fichier.readlines()
instruction = "[A-Z]{3}"
reg = "[0-9]"



    liste = i.split(",")
    print(liste)

    dico = {}
    dico["ADD"] = 1
    dico["SUB"] = 2
    regex_inst = re.compile(instruction)
    reg_re = re.compile(reg)

    instruction2 = regex_inst.findall(i)
    registre = reg_re.findall(i)
    print(instruction2)
    print(registre)

    if "r" in liste[1]:
        reg2 = 1
    else:
        reg2 = 0

    instruc = 0
    instruc +=  dico.get(instruction2[0]) << 27
    instruc +=  int(registre[0]) << 22
    instruc +=  reg2 << 21
    instruc +=  int(registre[1]) << 5
    instruc +=  int(registre[2])

    print(hex(instruc))