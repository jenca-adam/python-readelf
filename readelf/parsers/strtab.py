import io


class StrTab:
    def __init__(self, content, file, *_):
        self.content = content
        self.stream = io.BytesIO(self.content)
        self.strings = [string.decode("ascii") for string in content[1:].split(b"\x00")]

    def get_name(self, offset):
        self.stream.seek(offset)
        result = bytearray()
        while True:
            nb = self.stream.read(1)
            if nb == b"\x00" or not nb:
                break
            result.append(ord(nb))
        self.stream.seek(0)
        return bytes(result).decode("ascii")
