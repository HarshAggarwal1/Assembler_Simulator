# Performs Lexical Analysis on a line of code
import re
from utils.colors import bcolors

class Lexer:

    valid_tokens = [
            "VarDecl",
            "LabelDecl",
            "Inst",
            "RegOperand",
            "ImmOperand",
            "Symbol"
    ]
    
    valid_insts = []
    valid_regs = []

    def __populateValidWords(self):
        with open("data/instructions", 'r') as insts:
            for line in insts:
                if(line[0] != "#"):
                    inst, _, _ = line.split()
                    self.valid_insts.append(inst)

        for i in range(7):
            self.valid_regs.append("R" + str(i))
        self.valid_regs.append("FLAGS")

    def __init__(self):
        self.__populateValidWords()

    def tokenize(self, line_num, line):

        tokens = []

        words = line.split()
        for w in words:
            if(w == "var"):
                tokens.append([w, self.valid_tokens[0]])
            elif(w[-1] == ":" and re.match('^[0-9_a-zA-Z]*$', w[:-1])):
                tokens.append([w[:-1], self.valid_tokens[1]])
            elif(w in self.valid_insts):
                tokens.append([w, self.valid_tokens[2]])
            elif(w in self.valid_regs):
                tokens.append([w, self.valid_tokens[3]])
            elif(w[0] == "$"):
                if(re.match('^[0-9]*$', w[1:])):
                    tokens.append([w[1:], self.valid_tokens[4]])
                else:
                    print(bcolors.FAIL + "ERROR: Illegal Immidiate Format \"" + w + "\" found in line " + str(line_num) + "." + bcolors.ENDC + bcolors.OKCYAN + " Correct usage: $<number <=255 and >=0>" + bcolors.ENDC)
                    return None
            elif(re.match('^[0-9_a-zA-Z]*$', w)):
                tokens.append([w, self.valid_tokens[5]])
            else:
                print(bcolors.FAIL + "ERROR: Unknown keyword/symbol \"" + w + "\" found in line " + str(line_num) + bcolors.ENDC)
                return None
        
        return tokens