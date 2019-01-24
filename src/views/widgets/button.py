from collections import Callable

from urwid import AttrMap, LineBox, Text, WidgetWrap, connect_signal, emit_signal

CLICK_SIGNAL = "on_click"

class Button(Text):
    signals = [CLICK_SIGNAL]

    def __init__(self, text: str, callback: Callable):
        super().__init__(f"[{text}]", align="center")
        connect_signal(self, CLICK_SIGNAL, callback)
        # Glitch
        self._selectable = True

    def keypress(self, size, key):
        if key == "enter":
            emit_signal(self, CLICK_SIGNAL)
            return None

        return key
