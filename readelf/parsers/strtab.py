import io
from readelf.helpers import read_string


class StrTab:
    def __init__(self, content, file, *_):
        self.content = content
        self.stream = io.BytesIO(self.content)
        self.strings = [
            string.decode("ascii", errors="replace")
            for string in content[1:].split(b"\x00")
        ]

    def get_name(self, offset):
        self.stream.seek(offset)
        result = read_string(self.stream)
        self.stream.seek(0)
        return result.decode("ascii")
