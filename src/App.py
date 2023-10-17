import tkinter as tk
import numpy as np

from .canvas import Canvas


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-type', 'splash')
        self.title('Editor')
        self.geometry('1000x700')
        
        self.__build()
        self.__run()
        
    def __build(self):
        tools_frame = tk.Frame(master = self, height=700, width = 150, relief=tk.RIDGE)
        tools_frame.pack(side=tk.LEFT)

        canvas_frame = tk.Frame(master=self, borderwidth=1, height=700, width=850, relief=tk.RIDGE)
        canvas_frame.pack(side=tk.RIGHT)
        self.canvas = Canvas(master = canvas_frame, height=700, width=850,  bg='black')
        self.canvas.pack()

        DDA_button = tk.Button(master = tools_frame, text="DDA", height=2, width=10, command=lambda: self.__set_draw_mode("DDA"))
        DDA_button.place(x=20,y=20)
        
        bresenham_button = tk.Button(master = tools_frame, text="Bresenham", height=2, width=10, command=lambda: self.__set_draw_mode("Bresenham"))
        bresenham_button.place(x=20,y=70)

        wu_button = tk.Button(master = tools_frame, text="Wu", height=2, width=10, command=lambda: self.__set_draw_mode("Wu"))
        wu_button.place(x=20,y=120)

        self.mode_button = tk.Button(master = tools_frame, text="mode:\ndefault", height=2, width=10, command=self.__change_mode)
        self.mode_button.place(x=20,y=500)

        label = tk.Label(master = tools_frame, text = 'Рудьман Иван\n021701')
        label.place(x = 30,y = 650)
        

    def __set_draw_mode(self, mode):
        self.canvas.draw_mode = mode

    def __change_mode(self):
        self.canvas.debug_mode = not self.canvas.debug_mode
        self.mode_button['text'] = 'mode:\ndebug' if self.canvas.debug_mode else 'mode:\ndefault'
    

    def __run(self):
        self.mainloop()