# Performs Semantic Analysis on a line of code
from utils.colors import bcolors

class SemanticsAnalyser:

    InstsType = {}
    varibleDeclEnded = False
    
    def __init__(self):

        for aType in "ABCDEF":
            self.InstsType[aType] = []

        with open("data/instructions", 'r') as insts:
            for line in insts:
                if(line[0] != "#"):
                    inst, _, instType = line.split()
                    self.InstsType[instType].append(inst)

    def verifyVariableDecl(self, line_num, sentence_type):
        if(not self.varibleDeclEnded):
            if(sentence_type != "VarDecl_EP"):
                self.varibleDeclEnded = True
                return True
        else:
            if(sentence_type == "VarDecl_EP"):
                print(bcolors.FAIL + "ERROR: Variables must be declared at the beginning. Illegal declaration in line " + str(line_num) + "." + bcolors.ENDC)    
                return False
        return True

    def verifyInstTypeUsage(self, line_num, sentence_type, tokens):  
        instruction_name = tokens[0][0]
        if instruction_name not in self.InstsType[sentence_type]:
            print(bcolors.FAIL + "ERROR: \"" + instruction_name +"\" is not a Type \"" + sentence_type + "\" instruction. Used in line " + str(line_num) + "." + bcolors.ENDC)    
            return False
        return True

    def verifyTypeUsage(self, line_num, sentence_type, tokens):
        if sentence_type == "TypeA_EP":
            return self.verifyInstTypeUsage(line_num, "A", tokens)
        elif sentence_type == "TypeB_EP":
            return self.verifyInstTypeUsage(line_num, "B", tokens)
        elif sentence_type == "TypeC_EP":
            return self.verifyInstTypeUsage(line_num, "C", tokens)
        elif sentence_type == "TypeD_EP":
            return self.verifyInstTypeUsage(line_num, "D", tokens)
        elif sentence_type == "TypeE_EP":
            return self.verifyInstTypeUsage(line_num, "E", tokens)
        elif sentence_type == "TypeF_EP":
            return self.verifyInstTypeUsage(line_num, "F", tokens)
        elif sentence_type == "LTypeA_EP":
            return self.verifyInstTypeUsage(line_num, "A", tokens[1:])
        elif sentence_type == "LTypeB_EP":
            return self.verifyInstTypeUsage(line_num, "B", tokens[1:])
        elif sentence_type == "LTypeC_EP":
            return self.verifyInstTypeUsage(line_num, "C", tokens[1:])
        elif sentence_type == "LTypeD_EP":
            return self.verifyInstTypeUsage(line_num, "D", tokens[1:])
        elif sentence_type == "LTypeE_EP":
            return self.verifyInstTypeUsage(line_num, "E", tokens[1:])
        elif sentence_type == "LTypeF_EP":
            return self.verifyInstTypeUsage(line_num, "F", tokens[1:])
        return True

    def verifyFLAGSUsage(self, line_num, sentence_type, tokens):
        flags_used = False
        for t in tokens:
            if t[0] == "FLAGS" and t[1] == "RegOperand":
                flags_used = True
                break

        if(not flags_used):
            return True

        correct = True
        if(sentence_type == "TypeC_EP"):
            correct &= (tokens[0][0] == "mov" and tokens[1][0] != "FLAGS")
        elif(sentence_type == "LTypeC_EP"):
            correct &= (tokens[1][0] == "mov" and tokens[2][0] != "FLAGS")
        else:
            correct &= False    # Only valid instruction type which can access FLAGS is C

        if(not correct):
            print(bcolors.FAIL + "ERROR: Illegal usage of FLAGS register found in line " + str(line_num) + "." + bcolors.ENDC + bcolors.OKCYAN + " Correct usage: [label:] mov <reg> FLAGS" + bcolors.ENDC)

        return correct

    def verifyImmidiate(self, line_num, sentence_type, tokens):
        immVal = None
        if sentence_type == "TypeB_EP":
            immVal = int(tokens[2][0])
        if sentence_type == "LTypeB_EP":
            immVal = int(tokens[3][0])
        
        if(not immVal):
            return True

        if(immVal > 255):
            print(bcolors.FAIL + "ERROR: Illegal Immidiate value of \"" + str(immVal) + "\" at line number " + str(line_num) + "." + bcolors.ENDC + bcolors.OKCYAN + " Value must be between 0 and 255 inclusive." + bcolors.ENDC)
            return False
        return True

    def isValid(self, line_num, sentence_type, tokens):
        if(not sentence_type):
            return False

        valid = True
        valid &= self.verifyVariableDecl(line_num, sentence_type)
        valid &= self.verifyTypeUsage(line_num, sentence_type, tokens)
        valid &= self.verifyFLAGSUsage(line_num, sentence_type, tokens)
        valid &= self.verifyImmidiate(line_num, sentence_type, tokens)
        return valid