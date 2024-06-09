import sys
import Memory
import ExecutionEngine
import ProgramCounter
import RegisterFile
import matplotlib.pyplot as plt


def main():
    ReadFile = sys.stdin.read()
    Instructions = ReadFile.split("\n")
    Instructions = [i for i in Instructions if i != '']  # Changed Here
    memory = Memory.__Memory(Instructions)  # Memory object
    regFile = RegisterFile.__RegisterFile()  # RegisterFile object
    PC = ProgramCounter.__ProgramCounter(0)  # ProgramCounter object
    EE = ExecutionEngine.__ExecutionEngine(memory, regFile)  # ExecutionEngine object
    halted = False
    x = []
    y = []
    cycles = 0
    fetch = False
    fetchAt = 0
    while not halted:
        inst = memory.getData(PC.getValue())  # Taking inst. at particular PC from the memory
        memory.memory, regFile.registers, halted, nextPC, fetch, fetchAt = EE.execute(inst) 
        PC.dump() 
        regFile.dump()
        x.append(PC.getValue())
        y.append(cycles)
        if fetch:
            x.append(fetchAt)
            y.append(cycles)
        PC.update(nextPC)  # updating the value of PC
        EE.fetchAt = 0
        EE.fetch = False
        cycles += 1
    memory.dump()
    plt.title("Memory-Fetches v/s Cycles")
    plt.ylabel("Address")
    plt.xlabel("Cycles")
    plt.scatter(y, x)
    plt.savefig("plot.png")
    sys.exit()


if __name__ == '__main__':
    main()
