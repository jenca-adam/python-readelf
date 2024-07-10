class Memory:
    def __init__(self):
        self.items = {}
        self.index = 0

    def alloc(self, addr, section):
        self.items[addr] = (section.content, section)

    def seek(self, addr):
        self.index = addr

    def get_section(self):
        return self[self.index]

    def __getitem__(self, taddr):
        for addr, (_, section) in self.items.items():
            if addr <= taddr <= addr + section.size:
                return section

    def read(self, n):
        right_bound = self.index + n
        output = bytearray(n)
        for addr, (content, _) in self.items.items():
            start = max(addr - self.index, 0)
            if start > n or addr + len(content) < self.index:
                continue
            output[start : start + len(content)] = content[max(self.index - addr, 0) :]
        self.index += n
        output += b"\x00" * (max(n - len(output), 0))
        return bytes(output[:n])
