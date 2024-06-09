# Generates code and symbol table
from utils.colors import bcolors

class SymbolTable:

    varDecls = {}
    labelDecls = {}
    varUsage = []
    labelUsage = []

    def checkReDecl(self, symbol, line_num):
        if symbol in self.varDecls:
            print(bcolors.FAIL + "ERROR: Symbol \"" + symbol + "\" re-declared on line " + str(line_num) + ". " + bcolors.ENDC + bcolors.OKCYAN + "First declared as a variable." + bcolors.ENDC)
            exit(-1)
        elif symbol in self.labelDecls:
            print(bcolors.FAIL + "ERROR: Symbol \"" + symbol + "\" re-declared on line " + str(line_num) + ". " + bcolors.ENDC + bcolors.OKCYAN + "First declared as a label." + bcolors.ENDC)
            exit(-1)

    def addVarDecl(self, varName, line_num):
        self.checkReDecl(varName, line_num)
        self.varDecls[varName] = -1

    def resolveVarAddr(self, codeSize):
        for addr, varName in enumerate(self.varDecls.keys(), codeSize):
            self.varDecls[varName] = addr

    def addLabelDecl(self, labelName, instNum, line_num):
        self.checkReDecl(labelName, line_num)
        self.labelDecls[labelName] = instNum

    def addVarUsage(self, varName, instNum, line_num):
        self.varUsage.append([instNum, varName, line_num])

    def addLabelUsage(self, labelName, instNum, line_num):
        self.labelUsage.append([instNum, labelName, line_num])

class CodeGen:

    symbolTable = SymbolTable()
    generatedCode = []
    generatedInstTypes = []
    halted = False
    instNum = 0
    hasError = False

    def checkHalted(self):
        if(self.generatedCode[-1][0][0] != 'hlt'):
            print(bcolors.FAIL + "ERROR: Program must have its last instruction as \"hlt\"" + bcolors.ENDC)
            exit(-1)

    def checkCodeSize(self):
        if(self.instNum + len(self.symbolTable.varDecls) > 256):
            print(bcolors.FAIL + "ERROR: Program size must be less than or equall to 512 bytes" + bcolors.ENDC)
            exit(-1)

    def verifyFrontendPass(self):
        if self.hasError:
            print(bcolors.HEADER + bcolors.BOLD + "INFO: Code cannot be generated until previous frontend errors are resolved! Quitting!" + bcolors.ENDC) 
            exit(-1)

    def verifyCode(self):
        self.symbolTable.resolveVarAddr(self.instNum)
        self.verifyFrontendPass()
        self.checkHalted()
        self.checkCodeSize()

    def generate(self, line_num, frontendPass, sentenceType, tokens):
        self.hasError |= not frontendPass
        
        if(not self.hasError):

            if self.halted:     # There should be no instructions after halt
                print(bcolors.FAIL + "ERROR: Instructions found after \"hlt\" on line " + str(line_num) + "." + bcolors.ENDC)
                exit(-1)

            if sentenceType in ["TypeF_EP", "LTypeF_EP"]:  # Halt was just encountered
                self.halted = True             

            # Add declartions symbol table
            if sentenceType == "VarDecl_EP":
                self.symbolTable.addVarDecl(tokens[1][0], line_num)
            elif sentenceType == "Label_EP":
                self.symbolTable.addLabelDecl(tokens[0][0], (self.instNum), line_num)
            elif sentenceType in ["LTypeA_EP", "LTypeB_EP", "LTypeC_EP", "LTypeD_EP", "LTypeE_EP", "LTypeF_EP"]: # Label Instructions
                self.symbolTable.addLabelDecl(tokens[0][0], self.instNum, line_num)

            # Add usage symbol table
            if sentenceType == "TypeD_EP": # Loads and Stores
                self.symbolTable.addVarUsage(tokens[2][0], self.instNum, line_num)
            if sentenceType == "TypeE_EP": # Jumps
                self.symbolTable.addLabelUsage(tokens[1][0], self.instNum, line_num)
            elif sentenceType == "LTypeD_EP": # Loads and Stores
                self.symbolTable.addVarUsage(tokens[3][0], self.instNum, line_num)
            elif sentenceType == "LTypeE_EP": # Jumps
                self.symbolTable.addLabelUsage(tokens[2][0], self.instNum, line_num)
            
            # Generate code
            if sentenceType not in ["VarDecl_EP", "Label_EP"]:
                self.instNum += 1
                if sentenceType in ["TypeA_EP", "TypeB_EP", "TypeC_EP", "TypeD_EP", "TypeE_EP", "TypeF_EP"]:
                    self.generatedCode.append(tokens)
                    self.generatedInstTypes.append(sentenceType[4])
                else:
                    self.generatedCode.append(tokens[1:])
                    self.generatedInstTypes.append(sentenceType[5])