import re
import sys

fichier_asm = open(sys.argv[1], "r")
data = fichier_asm.readlines()
br = 0
addresse = 0

instruction_assembleur = [ "add", "sub", "mul", "div", "and",
                    "or", "xor", "shl", "shr", "slt", 
                    "sle", "seq", "load", "store", "jmp", 
                    "braz", "branz", "scall", "stop"    ] #Dictionnaire instruction

dictionnaire_inst = {}
donne_sortie = []
dictionnaire_de_labels = {}


for n in range(0, 19):
    dictionnaire_inst[instruction_assembleur[n]] = n + 1
print(len(dictionnaire_inst))
# add = 1, sub = 2, mul = 3, div = 4...



for i in data:
    tableau = []
    part_nombre_reg = []
    register = []
    
    


    for p in i:
        try:
            if p == "#":
                break
            if p == " ":
                continue
            elif p == "\n":
                break
            tableau.append(p)
        except ValueError:
            print("Erreur lors du traitement")

    tableau_virgule = "".join(tableau)

    if tableau_virgule == '':
        continue

    print(tableau_virgule)

    splitage_tableau = tableau_virgule.split(",") # On sépare en fonction des virgules
    if "jmp" in splitage_tableau[0]: # Si le premier instruction est jmp
        inst = "jmp"
        if "jmpr" in splitage_tableau[0]:
            imm = 0
        else:
            imm = 1
    else:
    # if splitage_tableau[0] != "jmp":
        inst = splitage_tableau[0].rsplit("r", 1)[0]
        print(inst)

    if ":" in tableau_virgule:
        dictionnaire_de_labels[splitage_tableau[0][:-1]] = br
        continue
        
    else:
        br += 1

    instr = 0

    if inst == "stop":
        instr += dictionnaire_inst.get(inst) << 27

    elif inst == "branz":
        instr += dictionnaire_inst.get(inst) << 27
        instr += int(splitage_tableau[0].rsplit("r", 1)[1]) << 22
        instr += int(dictionnaire_de_labels.get(splitage_tableau[1]))

    elif inst == "jmp":
        if "r" in splitage_tableau[0].split("p")[1]:
            part_nombre_reg.append(int(splitage_tableau[0].split("p")[1][1:]))
            imm = 0
        else:
            part_nombre_reg.append(int(splitage_tableau[0].split("p")[1]))
            imm = 1
        part_nombre_reg.append(int(splitage_tableau[1][1:]))

        instr += dictionnaire_inst.get(inst) << 27
        instr += imm << 26
        instr += int(part_nombre_reg[0]) << 5
        instr += int(part_nombre_reg[1])
       

    elif inst == "braz":
        instr += dictionnaire_inst.get(inst) << 27
        instr += int(splitage_tableau[0].rsplit("r", 1)[1]) << 22
        instr += int(dictionnaire_de_labels.get(splitage_tableau[1]))


  
    elif inst == "scall":
        pass

    

    
    else:
        register.append("r"+splitage_tableau[0].rsplit("r", 1)[1]) # On ajoute le chiffre à la lettre r qu'on a splitté précedemment
        register.append(splitage_tableau[1]) # registre milieu
        register.append(splitage_tableau[2][:2]) # registre de droite
        part_nombre_reg.append(int(register[0][1:]))
        if "r" in register[1]:
            print(register[1])
            part_nombre_reg.append(int(register[1][1:]))
            imm = 0
        else:
            part_nombre_reg.append(int(register[1]))
            imm = 1
        part_nombre_reg.append(int(register[2][1:]))
        
        # if register[1] != "r":
        #     part_nombre_reg.append(int(register[1]))
        #     cmd = 0
        # register.append(int(register[2][1:]))

        instr += dictionnaire_inst.get(inst) << 27
        instr += int(part_nombre_reg[0]) << 22
        instr += imm << 21
        instr += int(part_nombre_reg[1]) << 5
        instr += int(part_nombre_reg[2])

    print(splitage_tableau)

    donne_sortie.append(instr)


fichier_a_decoder = open(sys.argv[2], "a")
for m in donne_sortie:
    fichier_a_decoder.write("0x%08x" % addresse + " " + hex(m))
    fichier_a_decoder.write("\n")
fichier_a_decoder.close()


    
       
print(tableau)


    


