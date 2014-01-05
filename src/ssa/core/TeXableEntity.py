
class TeXableEntity:
    """A documented object

    TeXableEntity is a very simple base class for mathematics-based
    objects (such as FiniteStateMachine).  It is assumed that the
    first bit is pure mathematics (something to be placed inside an
    'align' environment).

    >>> t = TeXableEntity('x', 'The variable $x$')
    >>> t
    TeXableEntity(TeX='x', doc='The variable $x$')

    >>> t.TeX
    'x'

    >>> t.doc
    'The variable $x$'

    >>> eval(repr(t)) == t
    True
    """
    __initializer = 'TeXableEntity(TeX={TeX!r}, doc={doc!r})'
    def __init__(self, TeX=None, doc=None):
        self.TeX = TeX
        self.doc = doc

    def __repr__(self):
        return self.__initializer.format(**self.__dict__)

    def __str__(self):
        return str(self.doc)
    
    def __eq__(self, other):
        if isinstance(other, TeXableEntity):
            return self.TeX == other.TeX and self.doc == other.doc
        else:
            return False

if __name__ == '__main__':
    import doctest
    doctest.testmod()
