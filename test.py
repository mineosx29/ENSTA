from audioop import add
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
dico_2 = {}



for n in range(0, len(instruction_assembleur)):
    dictionnaire_inst[instruction_assembleur[n]] = n + 1
print(len(dictionnaire_inst))
# add = 1, sub = 2, mul = 3, div = 4...

def reperage_label(file):
    dico_lab = {}
    br = 0
    tab = []
    for m in file:
        tableau2 = []
        for p in m:
            try:
                if p == "#" or p == ";":
                    break
                if p == " ":
                    continue
                elif p == "\n":
                    break
                tableau2.append(p)
            except ValueError:
                print("Erreur lors du traitement")



        tableau_virgule = "".join(tableau2)

        if ':' in tableau_virgule:
            index = tableau_virgule.rfind(":")
            dico_lab[tableau_virgule[:index]] = br
        else:
            if '' != tableau_virgule:
                br = br + 1
            else:
                pass

        # if ":" in tableau_virgule:
        #     index = tableau_virgule.rfind(":")
        #     tableau_virgule = tableau_virgule[(index+1):]
        #     if '' != tableau_virgule:
        #         tab.append(tableau_virgule)
        # elif '' == tableau_virgule:
        #     continue
        # else:
        #     tab.append(tableau_virgule)
    print(dico_lab)

    return dico_lab


dictionnaire_de_labels =  reperage_label(data)
print(dictionnaire_de_labels)

for i in data:
    tableau = []
    part_nombre_reg = []
    register = []
    tab = []


    for p in i:
        try:
            if p == "#" or p == ";":
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
    splitage_tableau = tableau_virgule.split(",") # On sépare en fonction des virgules





    if "jmp" in splitage_tableau[0]: # Si le premier instruction est jmp
        inst = "jmp"
        if "jmpr" in splitage_tableau[0]:
            imm = 0
        else:
            imm = 1
        for key in dictionnaire_de_labels:
            if key in splitage_tableau[0]:
                imm = 1
                print("Label Trouvé")
                print(key)
                break
            else:
                imm = 0
                print("Pas de label trouvé")
    else:
    # if splitage_tableau[0] != "jmp":
        inst = splitage_tableau[0].rsplit("r", 1)[0]
        #print(inst)

    if ":" in tableau_virgule:
        dictionnaire_de_labels[splitage_tableau[0][:-1]] = br
        continue

    else:
        br += 1

    instr = 0

    if inst == "stop":
        instr += 0 << 27

    elif inst == "branz":
        instr += dictionnaire_inst.get(inst) << 27
        instr += int(splitage_tableau[0].rsplit("r", 1)[1]) << 22
        instr += int(dictionnaire_de_labels.get(splitage_tableau[1]))

    elif inst == "jmp":
        # if "r" in splitage_tableau[0].split("p")[1]:
        #     part_nombre_reg.append(int(splitage_tableau[0].split("p")[1][1:]))
        #     imm = 0
        # else:
        #     nombre_registre = int(splitage_tableau[0].split("p")[1])
        #     if nombre_registre < 0:
        #         nombre_registre = nombre_registre & (2**16)-1
        #     part_nombre_reg.append(nombre_registre)
        #     imm = 1
        if imm == 0:
            try:
               part_nombre_reg.append(int(splitage_tableau[0].split("p")[1][1:]))
            except ValueError:
                part_nombre_reg.append(int(splitage_tableau[0].split("p")[1]) & (2**16 - 1))
                imm = 1
        else:
            label = splitage_tableau[0][3:]
            #print(label)
            part_nombre_reg.append(dictionnaire_de_labels.get(label))



        part_nombre_reg.append(int(splitage_tableau[1][1:]))

        instr += dictionnaire_inst.get(inst) << 27
        instr += imm << 26
        instr += int(part_nombre_reg[0]) << 5
        instr += int(part_nombre_reg[1])


    elif inst == "braz":
        instr += dictionnaire_inst.get(inst) << 27
        instr += int(splitage_tableau[0].rsplit("r", 1)[1]) << 22
        instr += int(dictionnaire_de_labels.get(splitage_tableau[1]))



    elif  "scall" in inst:
        n = int(inst[5:]) # On prend tout ce qui est après scall
        instr += dictionnaire_inst.get(inst[:5]) << 27 # On recherche l'instruction dans le dictionnaire
        instr += n




    else:
        register.append("r"+splitage_tableau[0].rsplit("r", 1)[1]) # On ajoute le chiffre à la lettre r qu'on a splitté précedemment
        register.append(splitage_tableau[1]) # registre milieu
        register.append(splitage_tableau[2][:2]) # registre de droite
        part_nombre_reg.append(int(register[0][1:]))
        if "r" in register[1]:
            #print(register[1])
            part_nombre_reg.append(int(register[1][1:]))
            imm = 0
        else:
            nombre_registre_e = int(register[1])
            if nombre_registre_e < 0:
                nombre_registre_e = nombre_registre_e & (2**16)-1
            part_nombre_reg.append(nombre_registre_e)
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

    #print(splitage_tableau)

    donne_sortie.append(instr)


fichier_a_decoder = open(sys.argv[2], "a")
for m in donne_sortie:
    fichier_a_decoder.write(hex(m))
    fichier_a_decoder.write("\n")
    addresse = addresse + 1
fichier_a_decoder.close()




print(tableau)

#fichier_a_decoder.write("0x%08x" % addresse + " " + hex(m))
