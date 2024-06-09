# Populates symbols
from utils.colors import bcolors

class SymbolPopulator:

    symbolTable = None
    populatedCode = None

    def __init__(self, theSymbolTable, theGeneratedCode):
        self.symbolTable = theSymbolTable
        self.populatedCode = theGeneratedCode

    def resolveSymbols(self):

        # Populate variables
        for instNum, varName, line_num in self.symbolTable.varUsage:
            if varName in self.symbolTable.varDecls:

                symbolTokenIdx = -1
                for idx, token in self.populatedCode[instNum]:
                    if token[1] == "Symbol":
                        symbolTokenIdx = idx
                        break

                self.populatedCode[instNum][symbolTokenIdx][0] = self.symbolTable.varDecls[varName]

            else:
                if varName in self.symbolTable.labelDecls:
                    print(bcolors.FAIL + "ERROR: Label \"" + varName + "\" used as a variable on line " + str(line_num) + ". " + bcolors.ENDC)
                    exit(-1)
                else:
                    print(bcolors.FAIL + "ERROR: Variable \"" + varName + "\" is not defined on line " + str(line_num) + ". " + bcolors.ENDC)
                    exit(-1)

        # Populate labels
        for instNum, labelName, line_num in self.symbolTable.labelUsage:
            if labelName in self.symbolTable.labelDecls:

                symbolTokenIdx = -1
                for idx, token in self.populatedCode[instNum]:
                    if token[1] == "Symbol":
                        symbolTokenIdx = idx
                        break

                self.populatedCode[instNum][symbolTokenIdx][0] = self.symbolTable.labelDecls[labelName]

            else:
                if labelName in self.symbolTable.varDecls:
                    print(bcolors.FAIL + "ERROR: Variable \"" + labelName + "\" used as a label on line " + str(line_num) + ". " + bcolors.ENDC)
                    exit(-1)
                else:
                    print(bcolors.FAIL + "ERROR: Label \"" + labelName + "\" is not defined on line " + str(line_num) + ". " + bcolors.ENDC)
                    exit(-1)