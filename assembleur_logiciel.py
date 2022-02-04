import re
import sys

fichier_asm = open(sys.argv[1], "r")
data = fichier_asm.readlines()

instruction_assembleur = ["add", "sub", "mul", "div", "and", "or", "xor", "shl", "seq", "load", "store", "braz", "branz", "jmp", "stop"]

dictionnaire_inst = {}
donne_sortie = []
dictionnaire_de_labels = {}

for n in range(0, len(instruction_assembleur)):
    dictionnaire_inst[instruction_assembleur[n]] = n + 1
# add = 1, sub = 2, mul = 3, div = 4...

for i in data:
    tableau = []
    br = 0
    


    for p in i:
        if p == "#":
            break
        elif p == "\n":
            break
        elif p == " ":
            continue
        else:
            tableau.append(p)

    tableau_virgule = "".join(tableau)

    if tableau_virgule == '':
        continue

    

    splitage_tableau = tableau_virgule.split(",")
    if splitage_tableau[0] == "jmp":
        inst = "jmp"
        if splitage_tableau[0] == "jmpr":
            cmd = 1
        else:
            cmd = 0

    if splitage_tableau[0] != "jmp":
        inst = splitage_tableau[0].rsplit("r", 1)[0]
        print(inst)

    if splitage_tableau == ":" :
        dictionnaire_de_labels[splitage_tableau[0][-1]] = br
    elif splitage_tableau != ":":
        br += 1

    instr = 0

    if inst == "branz":
        instr += dictionnaire_inst.get(inst) << 27
        instr += int(splitage_tableau[0].rsplit("r", 1)[1]) << 22

    elif inst == "braz":
        instr += dictionnaire_inst.get(inst) << 27
        instr += int(splitage_tableau[0].rsplit("r", 1)[1]) << 22
    
    elif inst == "stop":
        instr += dictionnaire_inst.get(inst) << 27


    print(splitage_tableau)

    donne_sortie.append(instr)

for m in donne_sortie:
    print(hex(m))


    
       
print(tableau)


    