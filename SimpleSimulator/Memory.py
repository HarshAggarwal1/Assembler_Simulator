class __Memory:
    memory = []

    def __init__(self, arr):
        self.memory = ["0000000000000000"] * 256
        for i in range(len(arr)):
            self.memory[i] = arr[i]

    def dump(self):
        for item in self.memory:
            print(item)

    def getData(self, program_counter):
        return self.memory[program_counter]

    def update(self, program_counter, value):
        self.memory[program_counter] = "{:016b}".format(value)


def readFile(filename):
    f = open(filename, "r")   #
    inst = f.read().splitlines()
    f.close()
    return inst
