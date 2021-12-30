class Element:
    __no_content__ = False

    def __init__(self, content="", **kwargs):
        self.content = content
        self.kwargs = kwargs

    def attrs(self):
        return " ".join(f"{k}={v!r}" for k, v in self.kwargs.items())

    @staticmethod
    def fetch(content):
        return content.generate() if isinstance(content, Element) else content

    def generate(self):
        elem = type(self).__name__[7:].lower()
        return f"<{elem} {self.attrs()}" + ("/>" if self.__no_content__ else f">{self.fetch(self.content)}</{elem}>")

    def __radd__(self, other):
        return Element.fetch(other) + self.generate()

    def __add__(self, other):
        return self.generate() + Element.fetch(other)


class ElementA(Element):
    pass


class ElementU(Element):
    pass


class ElementStrong(Element):
    pass


class ElementH2(Element):
    pass


class ElementCenter(Element):
    pass


class ElementSpan(Element):
    pass


class ElementI(Element):
    pass


class ElementBr(Element):
    __no_content__ = True


class ElementDiv(Element):
    pass


class ElementTextArea(Element):
    pass
