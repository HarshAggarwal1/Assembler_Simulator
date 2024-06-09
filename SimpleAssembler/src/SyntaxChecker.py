# Performs Synatax Analysis on a line of code
from utils.colors import bcolors

class ParseTree:

    nodeTypes = {
        "StartNode"         : "StartNode",
        
        # All intermidiate nodes in AST
        "VarDecl"           : "VarDecl",
        "VarDeclSymbol"     : "Symbol",
        "LabelDecl"         : "LabelDecl",
        # Instructions without label
        "Instruction"       : "Inst",
        "RegOp1"            : "RegOperand",
        "RegOp2"            : "RegOperand",
        "RegOp3"            : "RegOperand",
        "ImmOp2"            : "ImmOperand",
        "SymbolOp1"         : "Symbol",
        "SymbolOp2"         : "Symbol", 
        # Instructions follwing LabelDecl
        "LInstruction"      : "Inst",
        "LRegOp1"           : "RegOperand",
        "LRegOp2"           : "RegOperand",
        "LRegOp3"           : "RegOperand",
        "LImmOp2"           : "ImmOperand", 
        "LSymbolOp1"        : "Symbol",
        "LSymbolOp2"        : "Symbol", 

        # All sentence types
        "VarDecl_EP"        : "Endpoint",
        "Label_EP"          : "Endpoint",
        "TypeA_EP"          : "Endpoint",
        "TypeB_EP"          : "Endpoint",
        "TypeC_EP"          : "Endpoint",
        "TypeD_EP"          : "Endpoint",
        "TypeE_EP"          : "Endpoint",
        "TypeF_EP"          : "Endpoint",
        "LTypeA_EP"         : "Endpoint",
        "LTypeB_EP"         : "Endpoint",
        "LTypeC_EP"         : "Endpoint",
        "LTypeD_EP"         : "Endpoint",
        "LTypeE_EP"         : "Endpoint",
        "LTypeF_EP"         : "Endpoint"
    }

    edges = {
        
        # All possible sentences
        "StartNode"         : ["VarDecl", "LabelDecl", "Instruction"],
        
        # Sentence: VarDecl Symbol
        "VarDecl"           : ["VarDeclSymbol"],
        "VarDeclSymbol"     : ["VarDecl_EP"],
        
        # Sentence: Label [Inst | ]
        "LabelDecl"         : ["Label_EP", "LInstruction"],
        # Sentence: Inst [ RegOp1 | SymbolOp1 | ]
        "LInstruction"      : ["LRegOp1", "LSymbolOp1", "LTypeF_EP"],
        # Sentence: SymbolOperand1
        "LSymbolOp1"        : ["LTypeE_EP"],
        # Sentence: RegOp1 [ RegOp2 | ImmOp2 | SymbolOp2 ]
        "LRegOp1"           : ["LRegOp2", "LImmOp2", "LSymbolOp2"],
        # Sentence: SymbolOp2
        "LSymbolOp2"        : ["LTypeD_EP"],
        # Sentence: ImmOp2
        "LImmOp2"           : ["LTypeB_EP"],
        # Sentence: RegOp2 [ RegOp3 | ]
        "LRegOp2"           : ["LRegOp3", "LTypeC_EP"],
        # Sentence: RegOp3
        "LRegOp3"           : ["LTypeA_EP"],
    
        # Sentence: Inst [ RegOp1 | SymbolOp1 | ]
        "Instruction"       : ["RegOp1", "SymbolOp1", "TypeF_EP"],
        # Sentence: SymbolOperand1
        "SymbolOp1"         : ["TypeE_EP"],
        # Sentence: RegOp1 [ RegOp2 | ImmOp2 | SymbolOp2 ]
        "RegOp1"            : ["RegOp2", "ImmOp2", "SymbolOp2"],
        # Sentence: SymbolOp2
        "SymbolOp2"         : ["TypeD_EP"],
        # Sentence: ImmOp2
        "ImmOp2"            : ["TypeB_EP"],
        # Sentence: RegOp2 [ RegOp3 | ]
        "RegOp2"            : ["RegOp3", "TypeC_EP"],
        # Sentence: RegOp3
        "RegOp3"            : ["TypeA_EP"]
    }

    def parse(self, line_num, tokens):
        
        # Create token stack
        token_types = [t[1] for t in tokens]
        token_types.reverse()
        curNode = "StartNode"

        while(token_types):
            curToken = token_types.pop()
            
            foundNextNode = False
            for nextNode in self.edges[curNode]:
                if(self.nodeTypes[nextNode] == curToken):
                    curNode = nextNode
                    foundNextNode = True

            if(not foundNextNode):
                print(bcolors.FAIL + "ERROR: Syntax error at line " + str(line_num) + bcolors.ENDC)
                return None

        endpointCount = 0
        endpoint = None
        for nextNode in self.edges[curNode]:
            if self.nodeTypes[nextNode] == "Endpoint":
                endpointCount += 1
                endpoint = nextNode
        if(endpointCount == 1):
            return endpoint

        print(bcolors.FAIL + "ERROR: Incomplete sentence at line " + str(line_num) + bcolors.ENDC)
        return None

class SyntaxChecker:

    parseTree = None

    def __init__(self):
        self.parseTree = ParseTree()

    def parse(self, line_num, tokens):
        if(not tokens):
            return None
        return self.parseTree.parse(line_num, tokens)