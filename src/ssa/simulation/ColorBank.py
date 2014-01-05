
class ColorBank:
    def __init__(self):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red   = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue  = (0, 0, 255)

    def set_color(self, name, red, green, blue):
        setattr(self, str(name), (red, green, blue))

    @classmethod
    def get_inverse(cls, color, alpha=1):
        inverses = [255 - c for c in color] + [alpha]
        return tuple((channel for channel in inverses))

    @classmethod
    def random(cls, r):
        return tuple((r.randint(0, 255) for i in range(3)))
