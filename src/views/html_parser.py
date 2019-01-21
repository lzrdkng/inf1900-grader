import bs4
from urwid import *

class TagException(Exception):
    pass

class Tag:

    names= dict()

    class New:

        def __init__(self, name):
            self.name = name

        def __call__(self, cls):
            Tag.names[self.name] = cls

    def __init__(self, tag):

        self.node = None
        self.parse(tag)

    @staticmethod
    def get_cls(child):
        return Tag.names[child.name]

    def to_urwid(self):
        return self.node

class RootTag(Tag):

    def parse(self, tag):

        l = []

        for child in tag.children:
            if not isinstance(child, bs4.element.NavigableString):
                cls = Tag.get_cls(child)
                l.append(cls(child).to_urwid())

        self.node = ListBox(l)

@Tag.New("p")
class ParagraphTag(Tag):

    def parse(self, tag):
        self.node = Text(tag.string)

@Tag.New("input")
class InputTag(Tag):

    def parse(self, tag):
        if tag["type"] == "int":
            self.node = IntEdit(tag["prompt"])
        else:
            self.node = Edit(tag["prompt"])


def main():
    with open("main_view.html", "r") as f:
        soup = bs4.BeautifulSoup(f.read(), "html.parser")

    real_root = None

    for root in soup.children:
        if root.name == "root":
            real_root = RootTag(root)

    return real_root

def unhandled_input(key):
    if key == 'q':
        raise ExitMainLoop()

if __name__ == "__main__":

    root = main()

    l = MainLoop(root.node, unhandled_input=unhandled_input)
    l.run()
