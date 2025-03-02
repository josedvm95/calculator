import collections
from typing import Optional, List

from kivy import Config
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ColorProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

Config.read("config.ini")
Config.write()

# Set the app size
Window.size = (320, 470)
Window.minimum_width = 320
Window.minimum_height = 470

MATH_SIGNS_DICT = {
    "+": ["+", ""],
    "-": ["-", ""],
    "÷": ["/", ""],
    "x": ["x", ""]
}
MATH_SIGNS = [inner_v for v in MATH_SIGNS_DICT.values() for inner_v in v] + list(MATH_SIGNS_DICT.keys())
MAX_DIGITS = 11
MAX_DECIMALS = 10
MAX_HISTORY = 20

# Designate our .kv design file
Builder.load_file("calculator.kv")


def to_int(num: str):
    result = None
    try:
        result = int(num)
    except ValueError:
        pass
    return result


def math_sign_lookup(sign: str):
    for idx, el in enumerate(MATH_SIGNS_DICT.values()):
        if sign in el:
            return list(MATH_SIGNS_DICT.keys())[idx]


# TODO: histórico de las últimas 20 operaciones

class HoverMixin:
    was_pressed = BooleanProperty(False)
    hover_color = ColorProperty()

    def __init__(self, **kwargs):
        self.is_hover = BooleanProperty(False)
        self.register_event_type('on_enter')  # noqa
        self.register_event_type('on_leave')  # noqa
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouseover)

    def on_mouseover(self, window, pos):
        is_inside = self.collide_point(*pos)  # noqa
        if self.is_hover == is_inside:
            if self.state == "normal" and self.was_pressed:  # noqa
                self.canvas.before.children[0].rgba = self.hover_color  # noqa
                self.was_pressed = BooleanProperty(False)
            return
        if is_inside:
            # on enter
            self.dispatch("on_enter")  # noqa
        else:
            # on leave
            self.dispatch("on_leave")  # noqa
        self.is_hover = is_inside

    def on_enter(self):
        ...

    def on_leave(self):
        ...

    def on_press(self):
        self.was_pressed = True


class HoverRoundedButton(HoverMixin, Button):
    """Only for square buttons"""
    hover_color = ColorProperty()
    init_color = ColorProperty()
    press_color = ColorProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        self.canvas.before.children[0].rgba = self.hover_color

    def on_leave(self):
        self.canvas.before.children[0].rgba = self.init_color


# TODO: show history button

class DisableRightClickMixin:
    def on_touch_down(self, touch):
        if touch.button == "left":
            return super().on_touch_down(touch)  # noqa


class DisableRightClickLayout(DisableRightClickMixin, GridLayout):
    pass  # do nothing


class MyLayout(Widget):

    def clear(self):
        self.ids.calc_input.text = "0"

    def remove(self):
        """Remove the last item in the textbox"""
        prior = self.ids.calc_input.text
        if len(prior) > 1:
            self.ids.calc_input.text = prior[:-1]
        else:
            self.ids.calc_input.text = "0"

    def on_key_down(self, keyboard, keycode, text, modifiers):
        command = self.command_keys.get(keyboard)
        app = App.get_running_app()
        prior = app.root.ids.calc_input.text
        if command == "backspace":
            if len(prior) == 1:
                app.root.ids.calc_input.text = "0"
            else:
                pass
        else:
            is_zero = False
            if prior == "0":
                is_zero = True
            prior = to_int(prior)
            try:
                number = to_int(text)
            except TypeError:
                # weird key, restore text
                return
            if is_zero and number is not None:
                app.root.ids.calc_input.text = ""
            if prior is None:
                app.root.ids.calc_input.text = app.root.ids.calc_input.text[:-1]
            else:
                app.root.ids.calc_input.text = app.root.ids.calc_input.text

    def on_key_up(self, keyboard, keycode):
        try:
            text = chr(keyboard)
        except ValueError:
            return  # weird key
        app = App.get_running_app()
        prior = app.root.ids.calc_input.text
        if len(prior) > 0:
            number = to_int(text)
            if number is None:
                app.root.ids.calc_input.text = prior.replace(text, "")
                if app.root.ids.calc_input.text == "":
                    app.root.ids.calc_input.text = "0"

    # Create a button pressing function
    def button_release(self, button):
        # create a variable that contains whatever was in the text box already
        prior = self.ids.calc_input.text

        number = to_int(button)
        if number is None:
            if button in MATH_SIGNS:
                self._math_sign(button)
            return

        # Test for error first
        if "ERROR" in prior:
            prior = ""

        if prior == "0":
            self.ids.calc_input.text = f"{number}"
        elif any(sign in prior for sign in MATH_SIGNS) or len(prior.replace(".", "")) < MAX_DIGITS:
            self.ids.calc_input.text = f"{prior}{number}"

    def negate(self):
        prior = self.ids.calc_input.text
        if "-" in prior:
            self.ids.calc_input.text = f"{prior.replace('-', '')}"
        elif prior != "0":
            self.ids.calc_input.text = f"-{prior}"

    # Create decimal function
    def dot(self):
        prior = self.ids.calc_input.text
        # Split our text box by +
        num_list = prior.split("+")

        if "." not in num_list[-1]:
            self.ids.calc_input.text = f"{prior}."

    # Create equals to function
    def equals(self):
        prior = self.ids.calc_input.text
        # Preprocess
        prior = prior.replace("x", "*")
        prior = prior.replace("÷", "/")
        prior = prior.replace(" ", "")
        # Error handling
        try:
            # Evaluate the math from the textbox
            answer = eval(prior)
        except ZeroDivisionError:
            self.ids.calc_input.text = "Math ERROR"
            return
        # Put thousand separator
        answer = f"{answer:,}".replace(",", " ")
        # Output the answer
        n_decimals = len(str(answer).split(".")[-1])
        n_digits = len(str(answer).replace(".", ""))

        if n_digits - n_decimals > MAX_DECIMALS:
            answer = "Math ERROR"
        elif n_digits > MAX_DIGITS:
            answer = f"{answer:.{MAX_DECIMALS - (n_digits - n_decimals)}}"
        elif n_decimals <= MAX_DECIMALS:
            answer = str(answer)
        else:
            answer = f"{answer:11.10f}"
        if "." in answer and int(answer.split(".")[-1]) == 0:
            answer = answer.split(".")[0]
        self.ids.calc_input.text = answer
        # save to history
        app = App.get_running_app()
        app.history.append(answer)

    def _math_sign(self, sign):
        prior = self.ids.calc_input.text
        if prior[-1] in MATH_SIGNS:
            prior = prior[:-1]
        self.ids.calc_input.text = f"{prior}{math_sign_lookup(sign)}"


class CalcHistory(collections.abc.MutableSequence):
    def __init__(self, max_history: int, init_history: Optional[List] = None):
        self.max_history = max_history
        self.history = list()
        if init_history is not None:
            self.extend(init_history)

    def check(self, v):
        return len(self.history) < self.max_history

    def __len__(self):
        return len(self.history)

    def __getitem__(self, i):
        return self.history[i]

    def __delitem__(self, i):
        del self.history[i]

    def __setitem__(self, i, v):
        self.history[i] = v

    def insert(self, i, v):
        if self.check(v):
            self.history.insert(i, v)

    def append(self, v):
        if not self.check(v):
            self.history = self.history[1:]
        self.history.append(v)

    def __str__(self):
        return str(self.history)

    def __repr__(self):
        return self.__str__()


class CalculatorApp(App):
    history = CalcHistory(MAX_HISTORY)

    def build(self):
        self.icon = "calculator.png"
        Window.clearcolor = (242 / 255, 244 / 255, 243 / 255, 1)
        Window.bind(on_key_down=MyLayout.on_key_down)
        Window.bind(on_key_up=MyLayout.on_key_up)
        return MyLayout()


if __name__ == "__main__":
    CalculatorApp().run()
