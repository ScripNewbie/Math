from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen


class MatrixScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Matrix())


class Matrix(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
