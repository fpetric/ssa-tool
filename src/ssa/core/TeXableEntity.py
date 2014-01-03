
class TeXableEntity:
    def __init__(self, TeX=None, doc=None):
        self._TeX = TeX
        self._doc = doc

    def __repr__(self):
        return str((str(self._TeX), str(self._doc)))

    def __str__(self):
        return str(self._doc)
