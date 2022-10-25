from kivy.uix.image import Image
from kivy.utils import get_color_from_hex as gc
from kivy.metrics import sp
from kivy.uix.label import Label


class Empty(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = gc("555555")
        self.opacity = 0.1
        self.display_label()
        self.bind(pos=self.change_ps, size=self.change_ps)

    def change_ps(self, *_):
        if hasattr(self, "label"):
            self.label.pos = self.pos
            self.label.size = self.size

    def display_label(self):
        self.label = Label(
            bold=True,
            font_size=sp(22),
            text=""
        )
        self.add_widget(self.label)

    def display_field(self):
        self.parent.parent.parent.manager.transition.direction = "left"

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.display_field()
        return super().on_touch_down(touch)


class GoldenRatioSelection(Empty):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = gc("FFD700")
        self.opacity = 1
        self.label.text = "Golden Ratio"

    def display_field(self):
        super().display_field()
        self.parent.parent.parent.manager.current = "GR"


class MatrixSelection(Empty):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = gc("55D7FF")
        self.opacity = 1
        self.label.text = "Matrix"

    def display_field(self):
        super().display_field()
        self.parent.parent.parent.manager.current = "Matrix"


class VectorSelection(Empty):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = gc("FF55FF")
        self.opacity = 1
        self.label.text = "Vector"

    def display_field(self):
        super().display_field()
        self.parent.parent.parent.manager.current = "Vector"
