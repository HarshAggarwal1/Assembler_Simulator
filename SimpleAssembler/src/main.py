# main assembler code
import sys

from Lexer import Lexer
from SyntaxChecker import SyntaxChecker
from SemanticsAnalyser import SemanticsAnalyser
from CodeGen import CodeGen
from SymbolPopulator import SymbolPopulator
from BinGen import BinGen

def main():
	lexer = Lexer()
	syntaxChecker = SyntaxChecker()
	semanticsAnalyser = SemanticsAnalyser()
	codeGen = CodeGen()
	
	# Pass through frontend and CodeGen
	for line_num, line in enumerate(sys.stdin, 1):
		if(not line.isspace()):
			tokens = lexer.tokenize(line_num, line)
			sentenceType = syntaxChecker.parse(line_num, tokens)
			frontendPass = semanticsAnalyser.isValid(line_num, sentenceType, tokens)
			codeGen.generate(line_num, frontendPass, sentenceType, tokens)

	# Populate Symbols
	codeGen.verifyCode()
	symbolPopulator = SymbolPopulator(codeGen.symbolTable, codeGen.generatedCode)
	symbolPopulator.resolveSymbols()
	
	# Dump binary
	binGen = BinGen(symbolPopulator.populatedCode, codeGen.generatedInstTypes)
	binGen.dump()


if __name__ == '__main__':
	main()