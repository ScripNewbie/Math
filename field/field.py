from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex as gc

from selection import (
    Empty,
    GoldenRatioSelection,
    MatrixSelection
)
from configuration import ROWS, COLS


class FieldScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Field())


class Field(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = "assets/MathBG.png"
        self.keep_ratio = False
        self.allow_stretch = True
        self.all_variable()
        self.display_title()
        self.display_grid()

    def all_variable(self):
        self.all_selection = [
            GoldenRatioSelection,
            MatrixSelection
        ]

    def display_title(self):
        self.label_background = Image(
            pos=(0, Window.height-dp(50)),
            size=(Window.width, dp(50)),
            color=gc("111111")
        )
        self.label = Label(
            pos=(0, Window.height-dp(50)),
            size=(Window.width, dp(50)),
            font_size=sp(32),
            text="JDM Math"
        )
        self.add_widget(self.label_background)
        self.add_widget(self.label)

    def display_grid(self):
        self.grid = GridLayout(
            size=(Window.width, Window.height-dp(50)),
            padding=dp(10),
            spacing=dp(10),
            rows=ROWS,
            cols=COLS
        )
        for i in range(COLS*ROWS):
            if i >= len(self.all_selection):
                self.grid.add_widget(Empty())
            else:
                self.grid.add_widget(self.all_selection[i]())
        self.add_widget(self.grid)
