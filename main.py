from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from field import FieldScreen
from goldenRatio import GoldenRatioScreen
from Matrix import MatrixScreen


class MathApp(App):

    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(FieldScreen(name="field"))
        self.sm.add_widget(GoldenRatioScreen(name="GR"))
        self.sm.add_widget(MatrixScreen(name="Matrix"))
        return self.sm


if __name__ == "__main__":
    MathApp().run()
