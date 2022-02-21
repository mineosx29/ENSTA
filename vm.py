
import sys
from numpy import zeros,array

class Virtual_Machine:
    def __init__(self, nombre_registre = 32):
        self.regs = [0 for _ in range(nombre_registre)]
        self.p_counter = 0
        self.prog = None
        self.reg1 = None
        self.reg2 = None
        self.reg3 = None
        self.imm = None
        self.memory = zeros(1024, int)
        self.running = False

    def fetch(self):
        instruction = self.prog[self.p_counter]
        self.p_counter += 1
        return instruction

    def decode(self, instr):
        instrNum = (instr &  0xF8000000) >> 27
        if instrNum == 15:
            self.imm = (instr & 0x4000000) >> 26
            self.reg1 = (instr & 0x3FFFFE0) >> 5
            self.reg2 = (instr & 0x1F)
        elif instrNum == 16 or instrNum == 17:
            self.reg1 = (instr & 0x7C00000) >> 22
            self.reg2 = (instr & 0x3FFFFF)
        elif instrNum == 18:
            self.reg1 = (instr & 0x7FFFFFF)
        else:
            self.reg1 = (instr & 0x7C00000) >> 22
            self.imm = (instr & 0x200000) >> 21
            self.reg2 = (instr & 0x1FFFE0) >> 5
            self.reg3 = (instr & 0x1F)
        return instrNum

    def codage_inst(self, instrNum):
        if (instrNum == 0):
            self.running = False
        elif (instrNum == 1):
            if (self.imm):
                print(f"add r{self.reg1} {self.reg2} r{self.reg3}")
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                self.regs[self.reg3] = self.regs[self.reg1] + self.reg2
            else:
                print(f"add r{self.reg1} r{self.reg2} r{self.reg3}")
                self.regs[self.reg3] = self.regs[self.reg1] + self.regs[self.reg2]
        elif (instrNum == 2):
            if(self.imm):
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                print(f"sub r{self.reg1} {self.reg2} r{self.reg3}")
                self.regs[self.reg3] = self.regs[self.reg1] - self.reg2
            else:
                print(f"sub r{self.reg1} r{self.reg2} r{self.reg3}")
                self.regs[self.reg3] = self.regs[self.reg1] - self.regs[self.reg2]
        elif (instrNum == 3):
            if(self.imm):
                print(f"mul r{self.reg1} {self.reg2} r{self.reg3}")
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                self.regs[self.reg3] = self.regs[self.reg1] * self.reg2
            else:
                print(f"mul r{self.reg1} r{self.reg2} r{self.reg3}")
                self.regs[self.reg3] = self.regs[self.reg1] * self.regs[self.reg2]
        elif (instrNum == 4):
            if(self.imm):
                print(f"div r{self.reg1} {self.reg2} r{self.reg3}")
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                try:
                    self.regs[self.reg3] = self.regs[self.reg1] / self.reg2
                except ZeroDivisionError:
                    pass
            else:
                print(f"div r{self.reg1} r{self.reg2} r{self.reg3}")
               
                try:
                    self.regs[self.reg3] = self.regs[self.reg1] / self.regs[self.reg2]
                except ZeroDivisionError:
                    pass
                        
        elif (instrNum == 5):
            if(self.imm):
                print(f"and r{self.reg1} {self.reg2} r{self.reg3}")
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                self.regs[self.reg3] = self.regs[self.reg1] & self.reg2
            else:
                print(f"and r{self.reg1} r{self.reg2} r{self.reg3}")
                self.regs[self.reg3] = self.regs[self.reg1] & self.regs[self.reg2]
        elif (instrNum == 6):
            if(self.imm):
                print(f"or r{self.reg1} {self.reg2} r{self.reg3}")
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                self.regs[self.reg3] = self.regs[self.reg1] | self.reg2
            else:
                print(f"or r{self.reg1} r{self.reg2} r{self.reg3}")
                self.regs[self.reg3] = self.regs[self.reg1] | self.regs[self.reg2]
        elif (instrNum == 7):
            if(self.imm):
                print(f"xor r{self.reg1} {self.reg2} r{self.reg3}")
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                self.regs[self.reg3] = self.regs[self.reg1] ^ self.reg2
            else:
                print(f"xor r{self.reg1} r{self.reg2} r{self.reg3}")
                self.regs[self.reg3] = self.regs[self.reg1] ^ self.regs[self.reg2]
        elif (instrNum == 8):
            if(self.imm):
                print(f"shl r{self.reg1} {self.reg2} r{self.reg3}")
                self.regs[self.reg3] = self.regs[self.reg1] >> self.reg2
            else:
                print(f"shl r{self.reg1} r{self.reg2} r{self.reg3}")
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                self.regs[self.reg3] = self.regs[self.reg1] >> self.regs[self.reg2]
        elif (instrNum == 9):
            if(self.imm):
                print(f"shr r{self.reg1} {self.reg2} r{self.reg3}")
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                self.regs[self.reg3] = self.regs[self.reg1] << self.reg2
            else:
                print(f"shr r{self.reg1} r{self.reg2} r{self.reg3}")
                self.regs[self.reg3] = self.regs[self.reg1] << self.regs[self.reg2]
        elif (instrNum == 10):
            if(self.imm):
                print(f"slt r{self.reg1} {self.reg2} r{self.reg3}")
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                if (self.regs[self.reg1] < self.reg2):
                    self.regs[self.reg3] = 1
                else:
                    self.regs[self.reg3] = 0
           
            else:
                print(f"slt r{self.reg1} r{self.reg2} r{self.reg3}")
                if (self.regs[self.reg1] < self.regs[self.reg2]):
                    self.regs[self.reg3] = 1
                else:
                    self.regs[self.reg3] = 0
        elif (instrNum == 12):
            if(self.imm):
                print(f"seq r{self.reg1} {self.reg2} r{self.reg3}")
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                if (self.regs[self.reg1] == self.reg2):
                    self.regs[self.reg3] = 1
                else:
                    self.regs[self.reg3] = 0
            else:
                print(f"seq r{self.reg1} r{self.reg2} r{self.reg3}")
                if (self.regs[self.reg1] == self.regs[self.reg2]):
                    self.regs[self.reg3] = 1
                else:
                    self.regs[self.reg3] = 0
        elif (instrNum == 13):
            if(self.imm):
                print(f"load r{self.reg1} {self.reg2} r{self.reg3}")
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                self.regs[self.reg3] = self.memory[self.regs[self.reg1] + self.reg2]
            else:
                print(f"load r{self.reg1} r{self.reg2} r{self.reg3}")
                self.regs[self.reg3] = self.memory[self.regs[self.reg1] + self.regs[self.reg2]]
        elif (instrNum == 14):
            if (self.imm):
                print(f"store r{self.reg1} {self.reg2} r{self.reg3}")
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                self.memory[self.regs[self.reg1] + self.reg2] = self.regs[self.reg3]
            else:
                print(f"store r{self.reg1} r{self.reg2} r{self.reg3}")
                self.memory[self.regs[self.reg1] + self.regs[self.reg2]] = self.regs[self.reg3]
                
        elif (instrNum == 15):
                if (self.imm):
                    print(f"jmp" + "r" + str(self.reg1) + ", r" + str(self.reg2))
                    if(self.reg1 < 0):
                        self.reg1 = self.reg1 & (2**16) -1
                    self.regs[self.reg2] = self.p_counter + 1
                    self.p_counter = self.reg1 - 1
                else:
                    print(f"jmp" + "r" + str(self.reg1) + ", r" + str(self.reg2))
                    self.regs[self.reg2] = self.p_counter + 1
                    self.p_counter = self.regs[self.reg1] - 1
        elif (instrNum == 16):
                print(f"braz  r{self.reg1}" + str(hex(self.reg2)))
                if self.regs[self.reg1] == 0:
                    self.p_counter = self.reg2 -1
                else:
                    pass
        

                


                

    def showRegs(self):
        res = "regs = "
        for i in range(len(self.regs)):
           print(" " ,self.regs[i])
        

    def run(self, prog, show_regs=True):
        self.prog = prog
        self.running = True
        while self.running:
            instruction = self.fetch()
            instrNum = self.decode(instruction)
            self.codage_inst(instrNum)
            if show_regs:
                self.showRegs()
        self.prog = None

if __name__ == "__main__":

    prog = [0x8200021, 0x7c0001c5]
    fichier_a_lire = open(sys.argv[1], "r")
    data1 = fichier_a_lire.readlines()
    
            

    print(prog)
    vm = Virtual_Machine(nombre_registre=32)
    vm.run(prog)




# if (self.regs[self.reg1] == self.regs[self.reg2]):
#                     self.regs[self.reg3] = 1
#                 else:
#                     self.regs[self.reg3] = 0
#                 self.regs[self.reg3] = self.memory[self.regs[self.reg1] + self.regs[self.reg2]]
