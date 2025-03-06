class AddrTab:
    def __init__(self, unit_length, address_size, segment_selector_size, entries):
        self.unit_length = unit_length
        self.address_size = address_size
        self.segment_selector_size = segment_selector_size
        self.entries = entries


class AddrTabs:
    def __init__(self, content):
        self.content = content
