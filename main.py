import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import math
from time import sleep

def ipart(x):
    return int(x)

def round(x):
    return int(x + 0.5)

def fpart(x):
    return x - int(x)

def rfpart(x):
    return 1 - fpart(x)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-type', 'splash')
        self.title('Editor')
        self.geometry('1000x700')
        self.positions = []
        self.lines = []
        self.isDraw: bool = False
        self.colors = np.ones(shape = (1000,700))
        self.mods = {'DDA' : self.draw_line_dda, 
                     'Bresenham': self.draw_line_bresenham,
                     'Wu': self.draw_line_wu_alt}
        self.draw_mode = 'DDA'
        self.debug_mode = False
        self.build()
        self.run()
        
    
    def build(self):
        tools_frame = tk.Frame(master = self, height=700, width = 150, relief=tk.RIDGE)
        tools_frame.pack(side=tk.LEFT)
        canvas_frame = tk.Frame(master=self, borderwidth=1, height=700, width=850, relief=tk.RIDGE)
        canvas_frame.pack(side=tk.RIGHT)
        self.canvas = tk.Canvas(master = canvas_frame, height=700, width=850,  bg='black')
        self.canvas.pack()

        DDA_button = tk.Button(master = tools_frame, text="DDA", height=2, width=10, command=lambda: self.set_draw_mode("DDA"))
        DDA_button.place(x=20,y=20)
        
        bresenham_button = tk.Button(master = tools_frame, text="Bresenham", height=2, width=10, command=lambda: self.set_draw_mode("Bresenham"))
        bresenham_button.place(x=20,y=70)

        wu_button = tk.Button(master = tools_frame, text="Wu", height=2, width=10, command=lambda: self.set_draw_mode("Wu"))
        wu_button.place(x=20,y=120)

        self.mode_button = tk.Button(master = tools_frame, text="mode:\ndefault", height=2, width=10, command=self.change_mode)
        self.mode_button.place(x=20,y=500)

        label = tk.Label(master = tools_frame, text = 'Рудьман Иван\n021701')
        label.place(x = 30,y = 650)
        
        self.canvas.bind('<Button-1>', self.position)
        self.canvas.bind('<Motion>', self.motion)



    def set_draw_mode(self, mode):
        self.draw_mode = mode

    def change_mode(self):
        self.debug_mode = not self.debug_mode
        self.mode_button['text'] = 'mode:\ndebug' if self.debug_mode else 'mode:\ndefault'
    
    def draw_line(self, *args):
        points = []
        for i in self.mods[self.draw_mode](*args):
            if self.debug_mode:
                sleep(0.005)
                self.update()
            points.append(self.draw_point(*i))
        return points


    def run(self):
        self.mainloop()

    
    def position(self, event):
        if self.isDraw:
            x, y = event.x, event.y
            if len(self.positions)>1:
                self.lines.append(self.draw_line(*self.positions[-1], x,y))
            self.isDraw = False
        else:
            x, y = event.x, event.y
            self.positions.append((x,y))
            self.lines.append(self.draw_line(x,y, x,y))
            self.isDraw = True
            

    def motion(self, event):
        if self.debug_mode:
            return
        if self.isDraw:
            if len(self.lines)>1:
                self.delete_last_line()
            if len(self.positions)>0:
                # self.canvas.create_line(*self.positions[-1], event.x, event.y)
                self.lines.append(self.draw_line(*self.positions[-1], event.x, event.y))


    def draw_point(self, x,y, alpha = 1):
        color = hex(int(255*(alpha)))[2:]*3
        return self.canvas.create_line(x,y,x+1,y, fill = f'#{color}')

    def draw_line_dda(self, x1,y1,x2,y2):
        #dda
        if x1-x2 == 0 and y1-y2==0:
            return [(x1,y1)]
        points = []
        lenght = max(abs(x1-x2), abs(y1-y2))
        dx = (x2-x1)/lenght
        dy = (y2-y1)/lenght
        x = x1
        y = y1
        i=0
        while i<lenght:
            x += dx
            y += dy
            points.append((x,y))
            i += 1
        return points
    
    def draw_line_bresenham(self, x1=0, y1=0, x2=0, y2=0):
        #Bresenham
        if x1-x2 == 0 and y1-y2==0:
            return [(x1,y1)]
        
        steep = abs(y2 - y1) > abs(x2 - x1)

        if abs(y2 - y1) > abs(x2 - x1):
            x1,y1 = y1,x1
            x2,y2 = y2,x2
        
        if x1>x2:
            x1,x2 = x2,x1
            y1,y2 = y2,y1

        ystep = 1 if y1 < y2 else -1

        points = []

        x,y = x1,y1
        dx = x2 - x1
        dy = abs(y2 - y1)
        e = 2*dy-dx
        i=1
        while i<dx:
            if e>0:
                y+=ystep
                e-=2*dx
            x+=1
            e+=2*dy
            i+=1
            if steep:
                points.append((y,x))
            else:
                points.append((x,y))

        return points

    def draw_line_wu_alt(self, x0, y0, x1, y1):
        if x0-x1 == 0 and y0-y1==0:
            return []
        
        steep = abs(y1 - y0) > abs(x1 - x0)

        if abs(y1 - y0) > abs(x1 - x0):
            x0,y0 = y0,x0
            x1,y1 = y1,x1
        
        if x0>x1:
            x0,x1 = x1,x0
            y0,y1 = y1,y0
        
        points = []

        if steep:
            points.append((y0,x0, 1))
        else:
            points.append((x1,y1,1 ))
        dx = x1 - x0
        dy = y1 - y0
        gradient = dy / dx
        y = y0 + gradient
        for x in range(x0+1, x1): 
            if steep:
                points.append((int(y), x, 1 - (y - int(y))))
                points.append((int(y) + 1, x, y - int(y)))
            else:
                points.append((x, int(y), 1 - (y - int(y))))
                points.append((x, int(y) + 1, y - (int(y))))
            
            y += gradient
        return points

    def delete_last_line(self):
        if len(self.lines)>0:
            for i in self.lines[-1]:
                self.canvas.delete(i)
            self.lines = self.lines[:-1]




App()