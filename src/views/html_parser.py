import bs4
from urwid import *
from widgets.grid import Grid
from widgets.button import Button

class TagException(Exception):
    pass

palette = (
    ("blue_head", "dark blue", ""),
    ("red_head", "dark red", ""),
    ("header", "bold, underline, brown", ""),
    ("error", "bold, light red", ""),
    ("normal_box", "default", "default"),
    ("selected_box", "black", "light gray"),
    ("confirm_button", "yellow", "dark blue"),
    ("abort_button", "light red", "brown"),
    ("progress_low", "default", "yellow"),
    ("progress_hight", "default", "dark green"),
    ("helper_key", "bold", "default"),
    ("helper_text_brown", "black", "brown"),
    ("helper_text_red", "black", "dark red"),
    ("helper_text_green", "black", "dark green"),
    ("helper_text_light", "white", "dark blue"),
    ("popup", "white", "dark blue"),
)


class Tag:

    names    = dict()
    classes  = dict()

    def __init__(self, tag):

        self.urwid = self.parse(tag)
        self.attr(tag)

        tag["node"] = self

    @staticmethod
    def get_cls(child):
        return Tag.names[child.name]

    def to_urwid(self):
        return self.urwid

    def attr(self, tag):
        if "class" in tag.attrs:
            for c in tag.attrs["class"]:
                if c in Tag.classes:
                    Tag.classes[c].set_attr(self)

class NewTag:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        Tag.names[self.name] = cls
        return cls

class NewClass:
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        Tag.classes[self.name] = cls
        return cls

@NewClass("linebox")
class LineBoxClass:

    @classmethod
    def set_attr(cls, self):
        self.urwid = LineBox(self.urwid)

@NewClass("header")
class HeaderClass:

    @classmethod
    def set_attr(cls, self):
        w = self.urwid.base_widget

        if not isinstance(w, Edit):
            raise TagException(f"Invalid class {cls} for widget {w}")

        w.set_caption(("header", w.caption))

@NewClass("confirm_button")
class ConfirmButtonClass:

    @classmethod
    def set_attr(cls, self):
        self.urwid = AttrMap(self.urwid, "default", "confirm_button")

@NewClass("abort_button")
class AbortButtonClass:

    @classmethod
    def set_attr(cls, self):
        self.urwid = AttrMap(self.urwid, "default", "abort_button")

@NewTag("div")
class DivTag(Tag):

    def parse(self, tag):

        l = []

        for child in tag.children:
            if not isinstance(child, bs4.element.NavigableString):
                cls = Tag.get_cls(child)
                l.append(cls(child).to_urwid())

        return ListBox(l)

@NewTag("row")
class RowTag(Tag):

    def parse(self, tag):

        row = []

        for child in tag.children:
            if not isinstance(child, bs4.element.NavigableString):
                cls = Tag.get_cls(child)
                row.append(cls(child).to_urwid())

        return row


@NewTag("grid")
class GridTag(Tag):

    def parse(self, tag):

        rows = []

        for child in tag.children:
            if not isinstance(child, bs4.element.NavigableString):
                cls = Tag.get_cls(child)
                rows.append(cls(child).to_urwid())

        return Grid(rows)


@NewTag("p")
class ParagraphTag(Tag):

    def parse(self, tag):
        return Text(tag.string)

@NewTag("edit")
class EditTag(Tag):

    def parse(self, tag):

        multiline = False

        if "multiline" in tag.attrs:
            multiline = True

        prompt = tag.string.strip().replace("\\n", "\n")

        # TODO type for IntEdit
        return Edit(caption=prompt, multiline=multiline)

    def attr(self, tag):

        if "default" in tag.attrs:
            self.urwid.insert_text(tag.attrs["default"])

        super().attr(tag)

@NewTag("button")
class ButtonTag(Tag):

    def parse(self, tag):

        callback = lambda *x: x

        if "on-click" in tag.attrs:
            callback = lambda: eval(tag.attrs["on-click"])

        return Button(tag.string, callback)


def main():
    with open("main_view.html", "r") as f:
        soup = bs4.BeautifulSoup(f.read(), "html.parser")

    root = None

    for child in soup.children:
        if not isinstance(child, bs4.element.NavigableString):
            if child.attrs["id"] == "root":
                root = DivTag(child).to_urwid()
            elif child.name == "config":
                generate_config()

    return root

def quit():
    raise ExitMainLoop()

def unhandled_input(key):
    if key == 'q':
        quit()

if __name__ == "__main__":

    root = main()

    l = MainLoop(root, palette, unhandled_input=unhandled_input)
    l.run()
