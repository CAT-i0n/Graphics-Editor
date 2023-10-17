import tkinter as tk
import numpy as np

from .canvas import Canvas

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-type', 'splash')
        self.title('Editor')
        self.geometry('1000x700')
        self.line_mods = ['DDA', 'Bresenham', 'Wu']
        self.line_mode_number = 0
        self.__build()
        self.__run()
        
    def __build(self):
        tools_frame = tk.Frame(master = self, height=700, width = 150, relief=tk.RIDGE)
        tools_frame.pack(side=tk.LEFT)

        canvas_frame = tk.Frame(master=self, borderwidth=1, height=700, width=850, relief=tk.RIDGE)
        canvas_frame.pack(side=tk.RIGHT)
        self._canvas = Canvas(master = canvas_frame, height=700, width=850,  bg='black')
        self._canvas.pack()

        self._line_button = tk.Button(master = tools_frame, text="Line:\nDDA", height=2, width=10, command=self.__change_line_draw_mode)
        self._line_button.place(x=20,y=20)

        circle_button = tk.Button(master = tools_frame, text="Circle", height=2, width=10, command=lambda: self.__change_draw_mode('Circle'))
        circle_button.place(x=20,y=70)

        ellipse_button = tk.Button(master = tools_frame, text="Ellipse", height=2, width=10, command=lambda: self.__change_draw_mode('Ellipse'))
        ellipse_button.place(x=20,y=120)

        hyperbola_button = tk.Button(master = tools_frame, text="Hyperbola", height=2, width=10, command=lambda: self.__change_draw_mode('Hyperbola'))
        hyperbola_button.place(x=20,y=170)

        parabola_button = tk.Button(master = tools_frame, text="Parabola", height=2, width=10, command=lambda: self.__change_draw_mode('Parabola'))
        parabola_button.place(x=20,y=220)
        
        
        self._mode_button = tk.Button(master = tools_frame, text="mode:\ndefault", height=2, width=10, command=self.__change_mode)
        self._mode_button.place(x=20,y=500)

        clear_button = tk.Button(master = tools_frame, text="Clear", height=2, width=10, command=self._canvas.clear)
        clear_button.place(x=20,y=550)

        

        label = tk.Label(master = tools_frame, text = 'Рудьман Иван\n021701')
        label.place(x = 30,y = 650)
        

    def __change_line_draw_mode(self):
        self.line_mode_number = (self.line_mode_number+1)%3
        self._canvas.draw_mode = self.line_mods[self.line_mode_number]
        self._line_button['text'] = 'Line:\n'+ self.line_mods[self.line_mode_number]

    def __change_draw_mode(self, mode):
        self._canvas.draw_mode = mode

    def __change_mode(self):
        self._canvas.debug_mode = not self._canvas.debug_mode
        self._mode_button['text'] = 'mode:\ndebug' if self._canvas.debug_mode else 'mode:\ndefault'
    

    def __run(self):
        self.mainloop()