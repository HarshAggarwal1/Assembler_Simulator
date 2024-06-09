# Dumps binary on stdout

class BinGen:

    populatedCode = None
    instTypes = None
    opcodeTable = {}
    regTable = {}

    def encode(self, num, length):
        numBin = bin(int(num))[2:]
        return "0" * (length - len(numBin)) + numBin

    def populateTables(self):

        with open("data/instructions", 'r') as insts:
            for line in insts:
                if(line[0] != "#"):
                    inst, opcode, instType = line.split()
                    self.opcodeTable[inst + instType] = opcode

        for i in range(7):
            regName = "R" + str(i)
            regBin = self.encode(i, 3)
            self.regTable[regName] = regBin
        self.regTable["FLAGS"] = self.encode(7, 3)


    def __init__(self, thePopulatedCode, theInstTypes):
        self.populatedCode = thePopulatedCode
        self.instTypes = theInstTypes
        self.populateTables()

    def handleA(self, tokens):
        print(self.opcodeTable[tokens[0][0] + "A"] + ("0"*2) +  self.regTable[tokens[1][0]] + self.regTable[tokens[2][0]] + self.regTable[tokens[3][0]], end="")

    def handleB(self, tokens):
        print(self.opcodeTable[tokens[0][0] + "B"] + self.regTable[tokens[1][0]] + self.encode(tokens[2][0], 8), end="")

    def handleC(self, tokens):
        print(self.opcodeTable[tokens[0][0] + "C"] + ("0"*5) + self.regTable[tokens[1][0]] + self.regTable[tokens[2][0]], end="")
    
    def handleD(self, tokens):
        print(self.opcodeTable[tokens[0][0] + "D"] + self.regTable[tokens[1][0]] + self.encode(tokens[2][0], 8), end="")

    def handleE(self, tokens):
        print(self.opcodeTable[tokens[0][0] + "E"] + ("0"*3) + self.encode(tokens[1][0], 8), end="")

    def handleF(self, tokens):
        print(self.opcodeTable['hltF'] + ("0"*11), end="")


    def dump(self):
        for tokens, instType in zip(self.populatedCode, self.instTypes):
            if instType == "A":
                self.handleA(tokens)
            elif instType == "B":
                self.handleB(tokens)
            elif instType == "C":
                self.handleC(tokens)
            elif instType == "D":
                self.handleD(tokens)
            elif instType == "E":
                self.handleE(tokens)
            elif instType == "F":
                self.handleF(tokens)
            print("")