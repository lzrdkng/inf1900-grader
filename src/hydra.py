#######################
# Authors:            #
#                     #
# Olivier Dion - 2019 #
#######################

class Head:

    def __init__(self, hydra, letter, func, hint="", exit_=None):

        self.hydra        = hydra
        self.exit_        = hydra.exit_
        self.func         = func
        self.hint         = hint
        self.letter       = letter

        if exit_ == Hydra.nil or exit_ == Hydra.t:
            self.exit_ = exit_

    def __str__(self):
        if self.hint != "":
            return "[{}]: {}".format(self.letter, self.hint)
        else:
            return self.letter

    def __call__(self):

        if self.func is not None:
            self.func()

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
                 foreign_keys=False, exit_=False,
                 color=None, **kwargs):

        for key in kwargs:
            self.__dict__[key] = kwargs[key]

        self.foreign_keys = foreign_keys
        self.exit_        = exit_
        self.info         = info
        self.heads        = {}
        self.name         = name

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

    def on_key(self, key):
        if key in self.heads:
            self.heads[key]()
        else:
            if self.foreign_keys == Hydra.warn:
                try:
                    self.on_warn()
                except AttributeError:
                    pass

    def add_heads(self, heads):
        for head in heads:

            letter = head[0]
            func   = head[1]
            hint   = ""
            exit_  = None

            try:
                hint = head[2]
                if not isinstance(hint, str):
                    hint = ""
            except:
                pass

            try:
                exit_ = head[3]

                if (exit_ != Hydra.nil and exit_ != Hydra.t):
                    exit_ = None
            except:
                pass

            self.heads[letter] = Head(self, letter, func, hint, exit_)

# For debugging
if __name__ == "__main__":

    heads = [
        ('g', None),
        ('H', None, "Hint"),
        ('q', None, "quit")
    ]

    hydra = Hydra(heads, "Infos!", color=Hydra.blue)

    print(str(hydra))
