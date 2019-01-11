#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

from urwid import Text

from src.views.base.tui import TUI

class HydraHead:

    def __init__(self, hydra, letter, func, hint="", exit_=None, params={}):

        self.hydra        = hydra
        self.exit_        = hydra.exit_
        self.func         = func
        self.hint         = hint
        self.letter       = letter
        self.params       = params

        if exit_ == Hydra.nil or exit_ == Hydra.t:
            self.exit_ = exit_

    def __str__(self):
        if self.hint != "":
            return "[{}]: {}".format(self.letter, self.hint)
        else:
            return self.letter

    def __call__(self):

        if self.func is not None:
            self.func(**self.params)

        if self.exit_ == Hydra.t:
            try:
                self.hydra.on_kill()
            except AttributeError:
                pass


class Hydra:

    # nil and true
    nil      = False
    t        = True

    # Colors
    red      = 1
    blue     = 2
    amaranth = 3
    teal     = 4
    pink     = 5

    # Foreign-keys
    warn     = 1
    run      = 2

    def __init__(self, name, heads, info="",
                 color=None, foreign_keys=False, exit_=False,
                 params={}):

        self.foreign_keys = foreign_keys
        self.exit_        = exit_
        self.info         = info
        self.heads        = {}
        self.name         = name
        self.params       = params

        if color == Hydra.red:
            pass

        elif color == Hydra.blue:
            self.exit_ = Hydra.t

        elif color == Hydra.amaranth:
            self.foreign_keys = Hydra.warn

        elif color == Hydra.teal:
            self.foreign_keys = Hydra.warn
            self.exit_        = Hydra.t

        elif color == Hydra.pink:
            self.foreign_keys = Hydra.run

        self.add_heads(heads)

    def __str__(self):

        heads_str = []

        for head_letter in self.heads:
            heads_str.append(str(self.heads[head_letter]))

        heads_str = ", ".join(heads_str)

        return "{}\n{}".format(self.info, heads_str)


    def __call__(self):
        self.func(**self.params)

    def add_heads(self, heads):

        for head in heads:

            letter = head[0]
            func   = head[1]
            hint   = ""
            exit_  = None
            params = {}

            try:
                hint = head[2]
                if not isinstance(hint, str):
                    hint = ""
            except:
                pass

            try:
                exit_ = head[3]

                if exit_ != Hydra.nil and exit_ != Hydra.t:
                    exit_ = None
            except:
                pass

            try:
                params = head[4]
                if not isinstance(params, dict):
                    params = {}
            except:
                pass

            self.heads[letter] = HydraHead(self, letter, func, hint, exit_, params)



class HydraWidget(Text):

    def __init__(self, hydra=None, *kargs, **kwargs):

        super().__init__("", *kargs, **kwargs)

        self.keybind = {}
        self.hydra   = hydra

        if hydra is not None:
            self.parse_hydra()

        # Glitch
        self._selectable = True

    def set_hydra(self):
        self.hydra = hydra
        self.parse_hydra()

    def parse_hydra(self):

        markup  = []

        # To refractor if better idea on how to make that

        markup.append(("", f"{self.hydra.info}\n"))

        for letter, head in self.hydra.heads.items():

            if head.exit_ == Hydra.t:
                tmp_letter = ("blue_head", head.letter)
            else:
                tmp_letter = ("red_head", head.letter)
            if head.hint != "":
                markup.append(("", "["))
                markup.append(tmp_letter)
                markup.append(("", f"]: {head.hint}"))
            else:
                markup.append(tmp_letter)

            markup.append(("", ", "))

        markup.pop()

        self.set_text(markup if len(markup) != 0 else "")

    def keypress(self, size, key):

        if key in self.hydra.heads:
            self.hydra.heads[key]()
            return None

        return key


    def add_heads(self, heads):
        if self.hydra is not None:
            self.hydra.add_heads(heads)
            self.parse_hydra()
