class __RegisterFile:
    registers = []

    def __init__(self):
        self.registers = ["0000000000000000"] * 8

    def update(self, reg, value):
        if reg == "R0":
            self.registers[0] = "{:016b}".format(value)
        elif reg == "R1":
            self.registers[1] = "{:016b}".format(value)
        elif reg == "R2":
            self.registers[2] = "{:016b}".format(value)
        elif reg == "R3":
            self.registers[3] = "{:016b}".format(value)
        elif reg == "R4":
            self.registers[4] = "{:016b}".format(value)
        elif reg == "R5":
            self.registers[5] = "{:016b}".format(value)
        elif reg == "R6":
            self.registers[6] = "{:016b}".format(value)
        elif reg == "FLAGS":
            self.registers[7] = "{:016b}".format(value)

    def getData(self, reg):
        if reg == "R0":
            return self.registers[0]
        elif reg == "R1":
            return self.registers[1]
        elif reg == "R2":
            return self.registers[2]
        elif reg == "R3":
            return self.registers[3]
        elif reg == "R4":
            return self.registers[4]
        elif reg == "R5":
            return self.registers[5]
        elif reg == "R6":
            return self.registers[6]
        elif reg == "FLAGS":
            return self.registers[7]

    def dump(self):
        for item in self.registers:
            print(item, end=" ")
        print()
