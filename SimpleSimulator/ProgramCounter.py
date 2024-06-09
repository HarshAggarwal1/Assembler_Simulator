class __ProgramCounter:
    pc = 0

    def __init__(self, pc):
        self.pc = pc

    def getValue(self):
        return self.pc

    def update(self, pc):
        self.pc = pc

    def dump(self):
        print("{:08b}".format(int(self.pc)), end=" ")
