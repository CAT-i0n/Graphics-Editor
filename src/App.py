import tkinter as tk
from tkinter import filedialog
from itertools import cycle

from .canvas import Canvas

from .modes import CanvasModes
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-type', 'splash')
        self.title('Editor')
        self.geometry('1000x700')
        self.line_mods = cycle(['DDA', 'Bresenham', 'Wu'])
        self.quadrtic_curves_mods = cycle(
            ['Circle', 'Ellipse', 'Hyperbola', 'Parabola'])
        self.curve_aproximation_mods = cycle(['Hermite', 'Bеzier', 'Splain', 'Closed splain'])
        self.poly_mods = ['Default', 'Graham', 'Jarvis', 'Delone']
        self.mods = cycle([CanvasModes.DRAW, CanvasModes.EDIT, CanvasModes.POLY, CanvasModes.FILL])
        self.__build()

    def __build(self):
        tools_frame = tk.Frame(master=self, height=700,
                               width=150, relief=tk.RIDGE)
        tools_frame.pack(side=tk.LEFT)

        canvas_frame = tk.Frame(
            master=self, borderwidth=1, height=700, width=850, relief=tk.RIDGE)
        canvas_frame.pack(side=tk.RIGHT)
        self._canvas = Canvas(master=canvas_frame,
                              height=700, width=850,  bg='black')
        self._canvas.main_parent = self
        self._canvas.pack()

        self._line_button = tk.Button(
            master=tools_frame, text="Line:\nDDA", height=2, width=12, command=self.__change_line_draw_mode)
        self._line_button.place(x=15, y=20)

        self._quadratic_curve_button = tk.Button(
            master=tools_frame, text="Quadratic Curve:\nCircle", height=2, width=12, command=self.__change_quadrtic_curve_draw_mode)
        self._quadratic_curve_button.place(x=15, y=70)

        self._curve_aproximation_button = tk.Button(
            master=tools_frame, text="Curve aproximation:\nHermite", height=2, width=12, command=self.__change_curve_aproximation_mode)
        self._curve_aproximation_button.place(x=15, y=120)


        poly_text = tk.Label(tools_frame, text = 'Poly')
        poly_text.place(x=15, y=165)

        self._poly_menu = tk.OptionMenu(
            tools_frame, self._canvas.poly_mode, *self.poly_mods)
        self._canvas.poly_mode.set('Default')
        self._poly_menu.config(height=1)
        self._poly_menu.config(width=10)
        self._poly_menu.place(x=15, y=185)


        check_poly_label = tk.Label(tools_frame, text = 'Полигон:\n', textvariable=self._canvas.poly_check)
        check_poly_label.place(x=15, y=300)


        color_text = tk.Label(tools_frame, text = 'Color')
        color_text.place(x=15, y=400)

        self._color = tk.Entry(master = tools_frame, width=14, textvariable=self._canvas.color_var)
        self._color.place(x=15, y=420)

        self._file_shape = tk.Button(
            master=tools_frame, text="select\nfile", height=2, width=12, command=lambda: self.__load_shape_from_file(filedialog.askopenfilename()))
        self._file_shape.place(x=15, y=450)

        self._mode_button = tk.Button(
            master=tools_frame, text="mode:\ndraw", height=2, width=12, command=self.__change_mode)
        self._mode_button.place(x=15, y=500)

        clear_button = tk.Button(
            master=tools_frame, text="Clear", height=2, width=12, command=self._canvas.clear)
        clear_button.place(x=15, y=550)

        self._canvas.is_debug = tk.BooleanVar()

        check_debug = tk.Checkbutton(tools_frame, text = "Debug", variable = self._canvas.is_debug, \
                    onvalue = True, offvalue = False)
        check_debug.place(x=35, y=600)

        label = tk.Label(master=tools_frame, text='Рудьман Иван\n021701')
        label.place(x=30, y=650)

    def __load_shape_from_file(self, path):
        shape = open(path).read()
        edges = shape.split('\n')[:-1]
        point_edges = list(map(lambda x: list(map(int, x[1:-1].split(','))), edges))
        print(point_edges)
        self._canvas.draw_poly_fig(point_edges)
        



    def __change_line_draw_mode(self):
        self._canvas.shape_draw_mode = next(self.line_mods)
        self._line_button['text'] = 'Line:\n' + self._canvas.shape_draw_mode
        self._canvas.change_draw_mode()

    def __change_quadrtic_curve_draw_mode(self):
        self._canvas.shape_draw_mode = next(self.quadrtic_curves_mods)
        self._quadratic_curve_button['text'] = 'Quadratic Curve:\n' + \
            self._canvas.shape_draw_mode
        self._canvas.change_draw_mode()

    def __change_curve_aproximation_mode(self):
        self._canvas.shape_draw_mode = next(self.curve_aproximation_mods)
        self._curve_aproximation_button['text'] = 'Curve aproximation:\n' + \
            self._canvas.shape_draw_mode
        self._canvas.change_draw_mode()
        
    def __change_mode(self):
        self._canvas.mode = next(self.mods)
        self._mode_button['text'] = 'mode:\n' + self._canvas.mode.value
        self._canvas.change_draw_mode()

    def run(self):
        next(self.quadrtic_curves_mods)
        next(self.line_mods)
        next(self.curve_aproximation_mods)
        next(self.mods)
        self.mainloop()
