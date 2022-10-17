from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as gc, platform
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.metrics import dp, sp
from kivy.uix.screenmanager import Screen


class MatrixScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Matrix())


class TxtInput(TextInput):

    def __init__(self, fsize=20, col=gc("222222"), **kwargs):
        super().__init__(**kwargs)
        self.input_filter = "int"
        self.text = "0"
        self.hint_text = "0"
        self.background_color = col
        self.foreground_color = gc("FFFFFF")
        self.font_size = sp(fsize)
        self.multiline = False


class Btton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = gc("888888")


class Slder(Slider):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.width = Window.width*0.1-dp(10)
        self.height = Window.height*0.6
        self.y = Window.height*0.2
        self.step = 1
        self.max = 20
        self.min = 1


class Lbel(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = gc("333333")
        self.height = sp(32)*2
        self.display_label()
        self.bind(pos=self.change_ps, size=self.change_ps)
        self.y = dp(100) + (0 if platform != "android" else dp(60))

    def change_ps(self, *_):
        if hasattr(self, "label"):
            self.label.pos = self.pos
            self.label.size = self.size

    def display_label(self):
        self.label = Label()
        self.label.text = "0"
        self.label.color = gc("55D7FF")
        self.label.font_size = sp(32)
        self.add_widget(self.label)


class Matrix(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = Window.size
        self.source = "assets/MathBG.png"
        self.keep_ratio = False
        self.allow_stretch = True
        self.all_variables()
        self.display_title()
        self.display_field()

    def all_variables(self):
        self.start_mat = 3
        self.grid_active = "1"
        self.change_size = Btton(text="Change Size")
        self.change_size.bind(on_release=self.change_size_func)
        self.addMatrix = Btton(text="Add Matrix")
        self.addMatrix.bind(on_release=self.addMatrix_func)
        self.minMatrix = Btton(text="Sub Matrix")
        self.minMatrix.bind(on_release=self.minMatrix_func)
        self.mulMatrix = Btton(text="Mul Matrix")
        self.mulMatrix.bind(on_release=self.mulMatrix_func)
        self.findDeter = Btton(text="Find Determinant")
        self.findDeter.bind(on_release=self.find_Deter_func)
        self.tools = [
            self.change_size,
            self.addMatrix,
            self.minMatrix,
            self.mulMatrix,
            self.findDeter
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
            text="Matrix"
        )
        self.add_widget(self.label_background)
        self.add_widget(self.label)

    def on_touch_down(self, touch):
        if self.label.collide_point(*touch.pos):
            self.parent.manager.transition.direction = "right"
            self.parent.manager.current = "field"
        return super().on_touch_down(touch)

    def display_field(self):
        self.grid = GridLayout(
            size=(Window.width*0.8, Window.height*0.6),
            pos=(Window.width*0.1, Window.height*0.2),
            padding=dp(5),
            spacing=dp(5),
            rows=self.start_mat,
            cols=self.start_mat
        )
        self.grid2 = GridLayout(
            size=(Window.width*0.8, Window.height*0.6),
            pos=(Window.width*0.1, Window.height*0.2),
            padding=dp(5),
            spacing=dp(5),
            rows=self.start_mat,
            cols=self.start_mat
        )
        self.switcher = Btton(
            text="Switch Matrix",
            size=(Window.width*0.8, dp(50)),
            pos=(self.grid.x, self.grid.top)
        )
        self.switcher.bind(on_release=self.switch_matrix)
        for _ in range(self.start_mat*self.start_mat):
            self.grid.add_widget(TxtInput(100/self.start_mat, gc("222222")))
            self.grid2.add_widget(TxtInput(100/self.start_mat, gc("444444")))
        self.add_widget(self.grid)
        self.add_widget(self.switcher)

        self.all_tools()

    def change_size_text(self, *_):
        self.change_size.text = f"[ {self.rslider.value}, {self.cslider.value} ]"

    def change_size_func(self, *_):
        if self.grid_active == "1":
            self.set_matrix_size(self.grid, self.cslider.value,
                                 self.rslider.value, gc("222222"))
        else:
            self.set_matrix_size(self.grid2, self.cslider.value,
                                 self.rslider.value, gc("444444"))

    def addMatrix_func(self, *_):
        if self.check_if_squareMatrix():
            for i in range(self.grid.cols*self.grid.rows):
                self.check_empty_matrix(i)
                self.grid.children[i].text = str(
                    int(self.grid.children[i].text) + int(self.grid2.children[i].text))
            self.last_step_eval()

    def minMatrix_func(self, *_):
        if self.check_if_squareMatrix():
            for i in range(self.grid.cols*self.grid.rows):
                self.check_empty_matrix(i)
                self.grid.children[i].text = str(
                    int(self.grid.children[i].text) - int(self.grid2.children[i].text))
            self.last_step_eval()

    def mulMatrix_func(self, *_):
        if self.grid.cols != self.grid2.rows:
            return
        self.matrix = list()
        for r in range(self.grid.rows):
            for c in range(self.grid2.cols):
                self.matrix.append(self.mulcolrowMat(r, c))
        self.set_matrix_size(self.grid, self.grid.rows,
                             self.grid2.cols, gc("222222"))
        self.setMatrix(self.matrix)
        self.last_step_eval()

    def setMatrix(self, li):
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                self.grid.children[
                    (r*self.grid.cols) + c].text = str(li[(r*self.grid.cols)+c])

    def mulcolrowMat(self, r, c):
        value = 0
        for i in range(self.grid.cols):
            self.check_empty_matrix((r*self.grid.cols) + i, 1)
            self.check_empty_matrix((i * self.grid2.cols) + c, 2)
            value += int(self.grid.children[(r*self.grid.cols) + i].text) * \
                int(self.grid2.children[(i * self.grid2.cols) + c].text)
        return value

    def check_empty_matrix(self, index, both=0):
        if both == 0 or both == 1:
            if self.grid.children[index].text == "":
                self.grid.children[index].text = "0"
        if both == 0 or both == 2:
            if self.grid2.children[index].text == "":
                self.grid2.children[index].text = "0"

    def check_if_squareMatrix(self):
        return (self.grid.rows == self.grid.rows and
                self.grid.cols == self.grid.cols)

    def all_tools(self):
        self.rslider = Slder(x=(dp(5)), value=self.start_mat)
        self.cslider = Slder(x=(Window.width*0.9+dp(5)), value=self.start_mat)
        self.rslider.bind(value=self.change_size_text)
        self.cslider.bind(value=self.change_size_text)
        self.grid_tools = GridLayout(
            size=(Window.width*0.8, Window.height*0.2),
            pos=(Window.width*0.1, 0),
            padding=dp(5),
            spacing=dp(5),
            rows=2,
            cols=4
        )
        for i in range(8):
            if i >= len(self.tools):
                self.grid_tools.add_widget(Btton())
            else:
                self.grid_tools.add_widget(self.tools[i])
        self.add_widget(self.rslider)
        self.add_widget(self.cslider)
        self.add_widget(self.grid_tools)

    def switch_matrix(self, *_):
        if self.grid in self.children:
            self.grid_active = "2"
            self.remove_widget(self.grid)
            self.add_widget(self.grid2)
        else:
            self.grid_active = "1"
            self.remove_widget(self.grid2)
            self.add_widget(self.grid)

    def last_step_eval(self):
        self.grid_active = "1"
        self.remove_widget(self.grid2)
        if self.grid not in self.children:
            self.add_widget(self.grid)

    def set_matrix_size(self, mat, col, row, color):
        mat.clear_widgets()
        mat.rows = row
        mat.cols = col
        for _ in range(col * row):
            mat.add_widget(TxtInput(100/row, color))

    def find_determinant(self, matrix, colSize):
        result = 0
        if colSize <= 2:
            result += matrix[0] * matrix[3]
            result -= matrix[1] * matrix[2]
            return result
        new_matrix = [0 for _ in range((colSize-1)*(colSize-1))]
        for i in range(colSize):
            index = 0
            for j in range(i):
                for k in range(colSize-1):
                    new_matrix[index + ((colSize-1)*k)
                               ] = matrix[j + (colSize * (k+1))]
                index += 1
            for j in range((colSize-1)-i):
                for k in range(colSize-1):
                    new_matrix[index+((colSize-1)*k)
                               ] = matrix[(i + j + 1) + (colSize * (k + 1))]
                index += 1
            if i % 2 == 0:
                result += matrix[i] * \
                    self.find_determinant(new_matrix, colSize-1)
            else:
                result -= matrix[i] * \
                    self.find_determinant(new_matrix, colSize-1)
        return result

    def find_Deter_func(self, *_):
        matrix = list()
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                self.check_empty_matrix((r*self.grid.cols)+c, 1)
                matrix.append(
                    int(self.grid.children[(r*self.grid.cols)+c].text))
        matrix = list(reversed(matrix))
        self.label.text = str(self.find_determinant(matrix, self.grid.cols))
