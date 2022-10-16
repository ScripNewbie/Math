from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from field import FieldScreen
from goldenRatio import GoldenRatioScreen


class MathApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_window()

    def setup_window(self):
        self._keyboard = Window.request_keyboard(self._keyboard_close, self)
        self._keyboard.bind(on_key_up=self._keyboard_down_key)

    def _keyboard_close(self):
        self._keyboard.unbind(on_key_down=self._keyboard_down_key)
        self._keyboard = None

    def _keyboard_down_key(self, _, key, *__):
        if key[1] == "escape":
            if self.sm.current != "field":
                self.sm.current = "field"

    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(FieldScreen(name="field"))
        self.sm.add_widget(GoldenRatioScreen(name="GR"))
        return self.sm


if __name__ == "__main__":
    MathApp().run()
