import numpy as np


class ColorPacker:
    @staticmethod
    def pack(color):
        r, g, b = np.array(color, dtype=np.uint8)
        code = r
        code = (code << 8)
        code += g
        code = (code << 8)
        code += b
        return code

    @staticmethod
    def unpack(packed_color):
        b = packed_color & 255
        g = (packed_color >> 8) & 255
        r = (packed_color >> 16) & 255
        return (r, g, b)
