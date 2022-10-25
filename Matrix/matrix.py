from os import system
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as gc, platform
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.animation import Animation
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
        self.font_size = sp(10) if platform == "android" else sp(16)
        self.background_color = gc("888888")


class Slder(Slider):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.cursor_image = ""
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
        self.label.color = gc("5588FF")
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
        self.addMatrix = Btton(text="Add")
        self.addMatrix.bind(on_release=self.addMatrix_func)
        self.minMatrix = Btton(text="Subtract")
        self.minMatrix.bind(on_release=self.minMatrix_func)
        self.divMatrix = Btton(text="Divide")
        self.divMatrix.bind(on_release=self.divMatrix_func)
        self.mulMatrix = Btton(text="Multiply")
        self.mulMatrix.bind(on_release=self.mulMatrix_func)
        self.findDeter = Btton(text="Determinant")
        self.findDeter.bind(on_release=self.find_Deter_func)
        self.findChild = Btton(text="Minors")
        self.findChild.bind(on_release=self.find_child_matrix)
        self.findCofactor = Btton(text="Cofactor")
        self.findCofactor.bind(on_release=self.get_cofactor)
        self.cramersRule = Btton(text="CramersR")
        self.cramersRule.bind(on_release=self.cramersRule_func)
        self.tools = [
            self.change_size,
            self.addMatrix,
            self.minMatrix,
            self.mulMatrix,
            self.divMatrix,
            self.findDeter,
            self.findChild,
            self.findCofactor,
            self.cramersRule
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
        if hasattr(self, "answer_label"):
            if self.answer_label.collide_point(*touch.pos):
                self.remove_widget(self.answer_label)
                self.remove_widget(self.answer_label_bg)
        return super().on_touch_down(touch)

    def display_field(self):
        self.grid = GridLayout(
            size=(Window.width*0.8, Window.height*0.6 if platform !=
                  "android" else Window.height*0.4),
            pos=(Window.width*0.1, Window.height*0.2 if platform !=
                 "android" else Window.height*0.3),
            padding=dp(5),
            spacing=dp(5),
            rows=self.start_mat,
            cols=self.start_mat
        )
        self.grid2 = GridLayout(
            size=(Window.width*0.8, Window.height*0.6 if platform !=
                  "android" else Window.height*0.4),
            pos=(Window.width*0.1, Window.height*0.2 if platform !=
                 "android" else Window.height*0.3),
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
            return
        self.message_alert(
            "Two matrices must have the same dimensions.")

    def minMatrix_func(self, *_):
        if self.check_if_squareMatrix():
            for i in range(self.grid.cols*self.grid.rows):
                self.check_empty_matrix(i)
                self.grid.children[i].text = str(
                    int(self.grid.children[i].text) - int(self.grid2.children[i].text))
            self.last_step_eval()
            return
        self.message_alert(
            "Two matrices must have the same dimensions.")

    def divMatrix_func(self, *_):
        if self.grid2.cols != self.grid2.rows:
            self.message_alert("Second matrix must be squared matrix.")
            return
        matrix = self.get_mat(self.grid2)
        deter = self.find_determinant(matrix, self.grid2.cols)
        if deter == 0:
            self.message_alert(
                "Second matrix determinant is Zero.")
            return
        for i in range(self.grid.cols*self.grid.rows):
            self.check_empty_matrix(i)
            self.grid.children[i].text = str(
                int(int(self.grid.children[i].text) / deter))
        self.last_step_eval()

    def mulMatrix_func(self, *_):
        if self.grid.cols != self.grid2.rows:
            self.message_alert(
                "Second matrix rows must be same on first cols.")
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
        return (self.grid.rows == self.grid2.rows and
                self.grid.cols == self.grid2.cols)

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
            rows=3,
            cols=3
        )
        for i in range(self.grid_tools.cols*self.grid_tools.rows):
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

    def find_child_matrix(self, *_):
        if self.grid.cols != self.grid.rows:
            self.message_alert("First matrix must be squared matrix.")
            return
        matrix = list()
        main_matrix = list()
        for rows in range(self.grid.rows):
            matr2 = list()
            for cols in range(self.grid.cols):
                self.check_empty_matrix((rows*self.grid.cols)+cols, 1)
                matr2.insert(
                    0, int(self.grid.children[(rows*self.grid.cols)+cols].text))
            matrix.insert(0, matr2)
        for rows in range(self.grid.rows):
            for cols in range(self.grid.cols):
                matr2 = list()
                for j in range(rows):
                    for k in range(cols):
                        matr2.append(matrix[j][k])
                for j in range(rows):
                    for k in range((self.grid.cols-1) - cols):
                        matr2.append(matrix[j][cols+k+1])
                for j in range((self.grid.rows-1)-rows):
                    for k in range(cols):
                        matr2.append(matrix[rows+1+j][k])
                for j in range((self.grid.rows-1)-rows):
                    for k in range((self.grid.cols-1)-cols):
                        matr2.append(matrix[rows+1+j][cols+1+k])
                main_matrix.insert(
                    0, self.find_determinant(matr2, self.grid.cols-1))
        self.set_matrix_size(self.grid, self.grid.rows,
                             self.grid.cols, gc("222222"))
        self.setMatrix(main_matrix)
        self.last_step_eval()

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

    def get_mat(self, grid):
        matrix = list()
        for r in range(grid.rows):
            for c in range(grid.cols):
                self.check_empty_matrix((r*grid.cols)+c, 1)
                matrix.insert(
                    0, int(grid.children[(r*grid.cols)+c].text))
        return matrix

    def find_Deter_func(self, *_):
        if self.grid.cols != self.grid.rows:
            self.message_alert("First matrix must be squared matrix.")
            return
        matrix = self.get_mat(self.grid)
        self.label.text = f"Determinant: {self.find_determinant(matrix, self.grid.cols)}"

    def get_cofactor(self, *_):
        if self.grid.cols != self.grid.rows:
            self.message_alert("First matrix must be squared matrix.")
            return
        adder = 0
        index = 1
        for i in range(self.grid.rows):
            adder = 0 if i % 2 == 0 else 1
            for j in range(self.grid.cols):
                index = 1 if (j + adder) % 2 == 0 else -1
                self.check_empty_matrix((i*self.grid.cols)+j, 1)
                self.grid.children[(i*self.grid.cols)+j].text = str(
                    int(self.grid.children[(i*self.grid.cols)+j].text) * index)
        self.last_step_eval()

    def cramersRule_func(self, *_):
        if self.grid.rows+1 != self.grid.cols:
            self.message_alert("First matrix must be augmented matrix.")
            return
        e_matrix = list()
        matrix = list()
        for rows in range(self.grid.rows):
            matr2 = list()
            for cols in range(self.grid.cols):
                self.check_empty_matrix((rows*self.grid.cols)+cols, 1)
                if cols == 0:
                    e_matrix.insert(
                        0, int(self.grid.children[(rows*self.grid.cols)+cols].text))
                    continue
                matr2.insert(
                    0, int(self.grid.children[(rows*self.grid.cols)+cols].text))
            matrix = matr2 + matrix
        main_deter = self.find_determinant(matrix, self.grid.cols-1)
        main_matrix = list()
        for cols in range(self.grid.cols-1):
            matr = list()
            matr += matrix
            for rows in range(self.grid.rows):
                matr[(rows*(self.grid.cols-1))+cols] = e_matrix[rows]
            determinant = self.find_determinant(
                matr, self.grid.cols-1)
            if main_deter == 0:
                if determinant == 0:
                    self.message_alert("Infinite Solution")
                    return
                continue
            main_matrix.append(self.find_determinant(
                matr, self.grid.cols-1) / main_deter)
        if main_deter == 0:
            self.message_alert("No Solution")
            return
        if hasattr(self, "answer_label"):
            self.remove_widget(self.answer_label)
            self.remove_widget(self.answer_label_bg)
        self.display_answer(main_matrix)

    def display_answer(self, answer):
        if not hasattr(self, "answer_label"):
            self.answer_label_bg = Image(
                size=(Window.width*0.8, Window.height*0.5),
                pos=(Window.width*0.1, Window.height*0.25),
                color=gc("222222")
            )
            self.answer_label = GridLayout(
                size=(Window.width*0.8, Window.height*0.5),
                pos=(Window.width*0.1, Window.height*0.25),
                cols=1,
                padding=dp(20),
                spacing=dp(20)
            )
        self.add_widget(self.answer_label_bg)
        self.add_widget(self.answer_label)
        self.answer_label.clear_widgets()
        self.answer_label.rows = len(answer)
        for i in range(len(answer)):
            label = Lbel()
            label.label.font_size = sp(120/len(answer))
            label.label.text = f"x{i+1} = {round(answer[i], 5)}"
            self.answer_label.add_widget(label)

    def message_alert(self, string="Error"):
        if not hasattr(self, "message"):
            self.message_bg = Image(
                color=gc("000000"),
                opacity=0.5,
                size=(Window.width, Window.height*0.1),
                pos=(0, Window.height*0.1)
            )
            self.message = Label(
                color=gc("5588FF"),
                font_size=sp(24),
                bold=True,
                size=(Window.width, Window.height*0.1),
                pos=(0, Window.height*0.1)
            )
            self.message_anim = Animation(opacity=0, d=2)
            self.add_widget(self.message_bg)
            self.add_widget(self.message)
        self.message_anim.cancel(self.message)
        self.message_anim.cancel(self.message_bg)
        self.message_bg.opacity = 0.5
        self.message.opacity = 1
        self.message.text = string
        self.message_anim.start(self.message)
        self.message_anim.start(self.message_bg)
