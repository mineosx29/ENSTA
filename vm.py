


class Virtual_Machine:
    def __init__(self, nombre_registre = 32):
        self.regs = [0 for _ in range(nombre_registre)]
        self.p_counter = 0
        self.prog = None
        self.reg1 = None
        self.reg2 = None
        self.reg3 = None
        self.imm = None
        self.running = False

    def fetch(self):
        instruction = self.prog[self.p_counter]
        self.p_counter += 1
        return instruction

    def decode(self, instr):
        instrNum = (instr &  0xF8000000) >> 27
        self.reg1 = (instr & 0x7C00000) >> 22
        self.reg2 = (instr & 0xFE0) >> 5
        self.reg3 = (instr & 0x1F)
        self.imm = (instr & 0x200000) >> 21
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
                print(f"add r{self.reg1} {self.reg2} r{self.reg3}")
                self.regs[self.reg3] = self.regs[self.reg1] + self.regs[self.reg2]
        elif (instrNum == 2):
            if(self.imm):
                print(f"sub r{self.reg1} {self.reg2} r{self.reg3}")
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                self.regs[self.reg3] = self.regs[self.reg1] - self.reg2
            else:
                print(f"sub r{self.reg1} {self.reg2} r{self.reg3}")
                self.regs[self.reg3] = self.regs[self.reg1] - self.regs[self.reg2]
        elif (instrNum == 3):
            if(self.imm):
                print(f"mul r{self.reg1} {self.reg2} r{self.reg3}")
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                self.regs[self.reg3] = self.regs[self.reg1] * self.reg2
            else:
                print(f"mul r{self.reg1} {self.reg2} r{self.reg3}")
                self.regs[self.reg3] = self.regs[self.reg1] * self.regs[self.reg2]
        elif (instrNum == 4):
            if(self.imm):
                print(f"div r{self.reg1} {self.reg2} r{self.reg3}")
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                self.regs[self.reg3] = self.regs[self.reg1] / self.reg2
            else:
                print(f"div r{self.reg1} {self.reg2} r{self.reg3}")
                self.regs[self.reg3] = self.regs[self.reg1] / self.regs[self.reg2]
        elif (instrNum == 5):
            if(self.imm):
                print(f"and r{self.reg1} {self.reg2} r{self.reg3}")
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                self.regs[self.reg3] = self.regs[self.reg1] & self.reg2
            else:
                print(f"and r{self.reg1} {self.reg2} r{self.reg3}")
                self.regs[self.reg3] = self.regs[self.reg1] & self.regs[self.reg2]
        elif (instrNum == 6):
            if(self.imm):
                print(f"or r{self.reg1} {self.reg2} r{self.reg3}")
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                self.regs[self.reg3] = self.regs[self.reg1] | self.reg2
            else:
                print(f"or r{self.reg1} {self.reg2} r{self.reg3}")
                self.regs[self.reg3] = self.regs[self.reg1] | self.regs[self.reg2]
        elif (instrNum == 7):
            if(self.imm):
                print(f"xor r{self.reg1} {self.reg2} r{self.reg3}")
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                self.regs[self.reg3] = self.regs[self.reg1] ^ self.reg2
            else:
                print(f"xor r{self.reg1} {self.reg2} r{self.reg3}")
                self.regs[self.reg3] = self.regs[self.reg1] ^ self.regs[self.reg2]
        elif (instrNum == 8):
            if(self.imm):
                print(f"shl r{self.reg1} {self.reg2} r{self.reg3}")
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                self.regs[self.reg3] = self.regs[self.reg1] >> self.reg2
            else:
                print(f"shl r{self.reg1} {self.reg2} r{self.reg3}")
                self.regs[self.reg3] = self.regs[self.reg1] >> self.regs[self.reg2]
        elif (instrNum == 9):
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
                if (self.reg2 < 0):
                    self.reg2 = self.reg2 & (2**16) -1
                if (self.regs[self.reg1] == self.regs[self.reg2]):
                    self.regs[self.reg3] = 1
                else:
                    self.regs[self.reg3] = 0
                    


