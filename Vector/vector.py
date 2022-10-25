from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex as gc, platform
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class VectorScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Vector())


class Vector(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = Window.size
        self.source = "assets/MathBG.png"
        self.keep_ratio = False
        self.allow_stretch = True
        self.display_title()

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
            text="Vector"
        )
        self.add_widget(self.label_background)
        self.add_widget(self.label)

    def on_touch_down(self, touch):
        if self.label.collide_point(*touch.pos):
            self.parent.manager.transition.direction = "right"
            self.parent.manager.current = "field"
