class __ExecutionEngine:
    isaDesc = {"00000": ["add", "A"], "00001": ["sub", "A"], "00010": ["mov", "B"], "00011": ["mov", "C"],
               "00100": ["ld", "D"], "00101": ["st", "D"], "00110": ["mul", "A"], "00111": ["div", "C"],
               "01000": ["rs", "B"], "01001": ["ls", "B"], "01010": ["xor", "A"], "01011": ["or", "A"],  # ISA description
               "01100": ["and", "A"], "01101": ["not", "C"], "01110": ["cmp", "C"], "01111": ["jmp", "E"],
               "10000": ["jlt", "E"], "10001": ["jgt", "E"], "10010": ["je", "E"], "10011": ["hlt", "F"]}

    reg = {"000": "R0", "001": "R1", "010": "R2", "011": "R3", "100": "R4", "101": "R5", "110": "R6", "111": "FLAGS"}  # registers description

    halted = False
    PC = 0
    fetch = False
    fetchAt = 0

    def __init__(self, memory, regFile):  # Constructor
        self.memory = memory
        self.regFile = regFile

    @staticmethod
    def B2D(binary):  # This static-method converts the binary into decimal
        i = 0
        decimal = 0
        for j in range(len(binary)):
            decimal += int(binary[len(binary) - 1 - j]) * (2 ** i)
            i += 1
        return decimal

    def execute(self, inst):  # This method takes instruction and executes it

        def typeA(ins):  # Type-A Instructions
            reg1 = ins[7:10]
            reg2 = ins[10:13]
            reg3 = ins[13:16]

            if self.isaDesc[ins[:5]][0] == "add":
                self.regFile.update("FLAGS", 0)
                num = self.B2D(self.regFile.getData(self.reg[reg2])) + self.B2D(self.regFile.getData(self.reg[reg3]))
                if num > 65535:
                    self.regFile.update("FLAGS", 8)
                x = "{:016b}".format(num)
                y = x[-16:]
                val = self.B2D(y)
                self.regFile.update(self.reg[reg1], val)

            elif self.isaDesc[ins[:5]][0] == "sub":
                self.regFile.update("FLAGS", 0)
                num = self.B2D(self.regFile.getData(self.reg[reg2])) - self.B2D(self.regFile.getData(self.reg[reg3]))
                if num < 0:
                    self.regFile.update("FLAGS", 8)
                    self.regFile.update(self.reg[reg1], 0)
                else:
                    self.regFile.update(self.reg[reg1], num)

            elif self.isaDesc[ins[:5]][0] == "mul":
                self.regFile.update("FLAGS", 0)
                num = self.B2D(self.regFile.getData(self.reg[reg2])) * self.B2D(self.regFile.getData(self.reg[reg3]))
                if num > 65535:
                    self.regFile.update("FLAGS", 8)
                x = "{:016b}".format(num)
                y = x[-16:]
                val = self.B2D(y) 
                self.regFile.update(self.reg[reg1], val)

            elif self.isaDesc[ins[:5]][0] == "xor":
                self.regFile.update("FLAGS", 0)
                value2 = self.B2D(self.regFile.getData(self.reg[reg2]))
                value3 = self.B2D(self.regFile.getData(self.reg[reg3]))
                value1 = value3 ^ value2
                self.regFile.update(self.reg[reg1], value1)

            elif self.isaDesc[ins[:5]][0] == "or":
                self.regFile.update("FLAGS", 0)
                value2 = self.B2D(self.regFile.getData(self.reg[reg2]))
                value3 = self.B2D(self.regFile.getData(self.reg[reg3]))
                value1 = value3 | value2
                self.regFile.update(self.reg[reg1], value1)

            elif self.isaDesc[ins[:5]][0] == "and":
                self.regFile.update("FLAGS", 0)
                value2 = self.B2D(self.regFile.getData(self.reg[reg2]))
                value3 = self.B2D(self.regFile.getData(self.reg[reg3]))
                value1 = value3 & value2
                self.regFile.update(self.reg[reg1], value1)

            self.PC += 1

        def typeB(ins):  # Type-B Instructions
            reg1 = ins[5:8] 
            imm_bin = ins[8:] 

            if self.isaDesc[ins[:5]][0] == "mov":
                self.regFile.update("FLAGS", 0)
                self.regFile.update(self.reg[reg1], self.B2D(imm_bin))

            elif self.isaDesc[ins[:5]][0] == "rs":
                self.regFile.update("FLAGS", 0)
                reg1_val = self.B2D(self.regFile.getData(self.reg[reg1]))
                rs_value = self.B2D(imm_bin)
                rightShifted = reg1_val >> rs_value
                self.regFile.update(self.reg[reg1], rightShifted)

            elif self.isaDesc[ins[:5]][0] == "ls":
                self.regFile.update("FLAGS", 0)
                reg1_val = self.B2D(self.regFile.getData(self.reg[reg1]))
                ls_value = self.B2D(imm_bin)
                leftShifted = reg1_val << ls_value
                self.regFile.update(self.reg[reg1], leftShifted)

            self.PC += 1

        def typeC(ins):  # Type-C Instructions
            reg1 = ins[10:13]
            reg2 = ins[13:16]

            if self.isaDesc[ins[:5]][0] == "mov":
                num = self.B2D(self.regFile.getData(self.reg[reg2]))
                self.regFile.update("FLAGS", 0)
                self.regFile.update(self.reg[reg1], num)

            elif self.isaDesc[ins[:5]][0] == "div":
                self.regFile.update("FLAGS", 0)
                rem = self.B2D(self.regFile.getData(self.reg[reg1])) % self.B2D(self.regFile.getData(self.reg[reg2]))  # remainder 
                quot = int(self.B2D(self.regFile.getData(self.reg[reg1])) / self.B2D(self.regFile.getData(self.reg[reg2])))  # quotient
                self.regFile.update("R0", quot)
                self.regFile.update("R1", rem)

            elif self.isaDesc[ins[:5]][0] == "not":
                self.regFile.update("FLAGS", 0)
                value = self.regFile.getData(self.reg[reg2])
                arr = []
                for i in range(len(value)):
                    arr.append(1 - int(value[i]))
                y = ""
                for item in arr:
                    y += f"{item}"
                not_value = self.B2D(y)
                self.regFile.update(self.reg[reg1], not_value)

            elif self.isaDesc[ins[:5]][0] == "cmp":
                self.regFile.update("FLAGS", 0)

                if self.B2D(self.regFile.getData(self.reg[reg1])) == self.B2D(self.regFile.getData(self.reg[reg2])):
                    self.regFile.update("FLAGS", 1)

                elif self.B2D(self.regFile.getData(self.reg[reg1])) > self.B2D(self.regFile.getData(self.reg[reg2])):
                    self.regFile.update("FLAGS", 2)

                elif self.B2D(self.regFile.getData(self.reg[reg1])) < self.B2D(self.regFile.getData(self.reg[reg2])):
                    self.regFile.update("FLAGS", 4)

            self.PC += 1

        def typeD(ins):  # Type-D Instructions
            reg1 = ins[5:8]
            mem_addr = ins[8:]
            addr = self.B2D(mem_addr)

            if self.isaDesc[ins[:5]][0] == "ld":
                self.regFile.update("FLAGS", 0)
                self.fetch = True
                self.fetchAt = addr
                value = self.B2D(self.memory.getData(addr))
                self.regFile.update(self.reg[reg1], value)

            elif self.isaDesc[ins[:5]][0] == "st":
                self.regFile.update("FLAGS", 0)
                self.fetch = True
                self.fetchAt = addr
                value = self.B2D(self.regFile.getData(self.reg[reg1]))
                self.memory.update(addr, value)

            self.PC += 1

        def typeE(ins):  # Type-E Instructions
            mem_addr = ins[8:]
            addr = self.B2D(mem_addr)

            if self.isaDesc[ins[:5]][0] == "jmp":
                self.regFile.update("FLAGS", 0)
                self.PC = addr

            elif self.isaDesc[ins[:5]][0] == "jlt":
                value = self.B2D(self.regFile.getData("FLAGS"))
                self.regFile.update("FLAGS", 0)
                if value == 4:
                    self.PC = addr
                else:
                    self.PC += 1

            elif self.isaDesc[ins[:5]][0] == "jgt":
                value = self.B2D(self.regFile.getData("FLAGS"))
                self.regFile.update("FLAGS", 0)
                if value == 2:
                    self.PC = addr
                else:
                    self.PC += 1

            elif self.isaDesc[ins[:5]][0] == "je":
                value = self.B2D(self.regFile.getData("FLAGS"))
                self.regFile.update("FLAGS", 0)
                if value == 1:
                    self.PC = addr
                else:
                    self.PC += 1

        if self.isaDesc[inst[:5]][1] == "A":
            typeA(inst)
        elif self.isaDesc[inst[:5]][1] == "B":
            typeB(inst)
        elif self.isaDesc[inst[:5]][1] == "C":
            typeC(inst)
        elif self.isaDesc[inst[:5]][1] == "D":
            typeD(inst)
        elif self.isaDesc[inst[:5]][1] == "E":
            typeE(inst)
        elif self.isaDesc[inst[:5]][1] == "F":
            self.regFile.update("FLAGS", 0)  # Changed Here
            self.halted = True

        return self.memory.memory, self.regFile.registers, self.halted, self.PC, self.fetch, self.fetchAt
