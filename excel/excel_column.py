class ExcelColumn:
    def __init__(self, key, header, value, style_handler=None):
        self.key = key
        self.header = header
        self.value = value
        self.style_handler = style_handler
