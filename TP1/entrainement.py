import numpy as np

class Entrainement:

    def __init__(self, window_scale, encoding, path) -> None:
        self.window = int(window_scale)
        self.encoding = encoding
        self.path = path