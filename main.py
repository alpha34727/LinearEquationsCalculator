import math
import tkinter as tk
from tkinter import ttk, Tk, IntVar
from tkextrafont import Font

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.pyplot import MultipleLocator
from matplotlib.backend_bases import _Mode

from phrase import phrase_equation
from fraction_calc import *

class NavigationToolbar2Ttk(NavigationToolbar2Tk):
    def __init__(self, canvas, window, pack_toolbar=False):
        super().__init__(canvas, window, pack_toolbar=False)
        self.message = tk.StringVar(master=self)
        self._message_label = ttk.Label(master=self, textvariable=self.message, justify=tk.RIGHT, style="TLabel")
        self._message_label.pack(side=tk.RIGHT)

        self.config(background="#FFFFFF")

    def _Button(self, text, image_file, toggle, command):
        if tk.TkVersion >= 8.6:
            PhotoImage = tk.PhotoImage
        else:
            from PIL.ImageTk import PhotoImage
        if image_file is not None:
            img = PhotoImage(master=self, file=image_file)
        else:
            img = None
        if not toggle:
            b = ttk.Button(
                master=self, text=text, command=command, image=img, style="TButton"
            )
            
        else:
            var = IntVar(master=self)
            b = ttk.Checkbutton(
                master=self, text=text, command=command, image=img, style="TCheckbutton", variable=var
            )
            b.var = var
        b._ntimage = img
        b.pack(side='left', padx=3)
        return b

    def _Spacer(self):
        s = ttk.Frame(master=self, height='18p', relief=tk.RIDGE, style="TFrame")
        s.pack(side=tk.LEFT, padx='5p')
        return s

    def _update_buttons_checked(self):
        for text, mode in [("Zoom", _Mode.ZOOM), ("Pan", _Mode.PAN)]:
            if text in self._buttons:
                if self.mode == mode:
                    self._buttons[text].var.set(1)
                else:
                    self._buttons[text].var.set(0)

root_width = 800
root_height = 480

def resize(event):
    if str(event.widget) == '.':
        global root_width
        global root_height
        if event.width != root_width or event.height != root_height:
            root_width = event.width
            root_height = event.height
            global default_font
            global math_font

            size = int(event.width*event.height/32000 + 4)
            if size > 28:
                size = 28
            elif size < 12:
                size = 12
            default_font.config(size=size)
            math_font.config(size=size)

def calc():
    line.clear()
    line.set_xlabel("x", loc='right')
    line.set_ylabel("y", loc='top')

    a1, b1, c1 = phrase_equation(input1.get())
    a2, b2, c2 = phrase_equation(input2.get())

    d = subtract(mutiply(a1, b2), mutiply(a2, b1))
    dx = subtract(mutiply(c1, b2), mutiply(c2, b1))
    dy = subtract(mutiply(a1, c2), mutiply(a2, c1))

    label_d['text'] = f'Δ = {simply_to_str(d)}'
    label_dx['text'] = f'Δx = {simply_to_str(dx)}'
    label_dy['text'] = f'Δy = {simply_to_str(dy)}'

    line.axhline(y=0, color="#000000")
    line.axvline(x=0, color="#000000")

    x = math.nan
    y = math.nan
    x_str = ""
    y_str = ""

    if d[0] == 0:
        if dx[0] == 0 and dy[0] == 0:
            label_situaltion['text'] = '無限多組解'
        else:
            label_situaltion['text'] = '無解'

        line.axline((0, simply_to_numerical(divide(c1, b1))), (1, simply_to_numerical(divide(subtract(c1, a1), b1))), color="#4fc3f7", label=input1.get())
        line.axline((0, simply_to_numerical(divide(c2, b2))), (1, simply_to_numerical(divide(subtract(c2, a2), b2))), color="#ffb74d", label=input2.get())
        line.grid(which='major')
    else:
        label_situaltion['text'] = '洽有一組解'
        x = divide(dx, d)
        y = divide(dy, d)
        x_str = simply_to_str(x)
        y_str = simply_to_str(y)
        line.axline((0, simply_to_numerical(divide(c1, b1))), (simply_to_numerical(divide(c1, a1)), 0), color="#4fc3f7", label=input1.get())
        line.axline((0, simply_to_numerical(divide(c2, b2))), (simply_to_numerical(divide(c2, a2)), 0), color="#ffb74d", label=input2.get())
        # line.axline((simply_to_numerical(divide(dx, d)), simply_to_numerical(divide(dy, d))), (simply_to_numerical(divide(dx, d))+1, simply_to_numerical(divide(subtract(c1, mutiply(a1, add(divide(dx, d), [1, 1]))), b1))), color="#4fc3f7", label=input1.get())
        # line.axline((simply_to_numerical(divide(dx, d)), simply_to_numerical(divide(dy, d))), (simply_to_numerical(divide(dx, d))+1, simply_to_numerical(divide(subtract(c2, mutiply(a2, add(divide(dx, d), [1, 1]))), b2))), color="#ffb74d", label=input2.get())
        line.grid(which='major')
        # print(simply_to_numerical(divide(dx, d)), simply_to_numerical(divide(dy, d)))
        line.plot(simply_to_numerical(divide(dx, d)), simply_to_numerical(divide(dy, d)), 'o', color="#ef5350")
    
    label_x['text'] = f'x = {x_str}'
    label_y['text'] = f'y = {y_str}'
    labels = [input1.get(), input2.get()]
    handles, _ = line.get_legend_handles_labels()
    line.legend(handles = handles, labels = labels, loc='upper right')
    line.xaxis.set_major_locator(MultipleLocator(1))
    line.yaxis.set_major_locator(MultipleLocator(1))
    
    canvas.draw()

root = Tk()
root.title("二元一次方程式計算機")
root.geometry(f"800x480")
root.config(background="#FFFFFF", padx=10, pady=10)

default_font = Font(file="./font/NotoSansTC-Regular.otf", family="Noto Sans TC", size=16)
math_font = Font(file="./font/STIXTwoText-Medium.otf", family="STIX Two Text Medium", size=16)

style = ttk.Style()
style.configure("TFrame", background="#FFFFFF")
style.configure("TCheckbutton", background="#FFFFFF")
style.configure("TLabel", background="#FFFFFF", font=default_font)
style.configure("Toolbar.TLabel", background="#FFFFFF", font=Font(family="STIX Two Text Medium", size=64))
style.configure("TButton", background="#FFFFFF", font=default_font)
style.configure("Math.TLabel", background="#FFFFFF", font=math_font)
style.configure("Math.TButton", background="#FFFFFF", font=math_font)
style.configure("TEntry", background="#FFFFFF")

info_frame = ttk.Frame(root, style="TFrame")

graph_frame = ttk.Frame(info_frame, style="TFrame")

fig = Figure(figsize=(8, 5), dpi=100)
line = fig.add_subplot()

canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.draw()

toolbar = NavigationToolbar2Ttk(canvas, graph_frame, pack_toolbar=True)
toolbar.update()

canvas.mpl_connect("key_press_event", key_press_handler)

toolbar.pack(fill='x', expand=True, side='top')
canvas.get_tk_widget().pack(fill='both', expand=True, side='bottom')

graph_frame.place(relwidth=0.8, relheight=1)

answer_frame = ttk.Frame(info_frame, style="TFrame")

label_d = ttk.Label(answer_frame, style="Math.TLabel")
label_d.pack(anchor='w')
label_dx = ttk.Label(answer_frame, style="Math.TLabel")
label_dx.pack(anchor='w')
label_dy = ttk.Label(answer_frame, style="Math.TLabel")
label_dy.pack(anchor='w')
label_situaltion = ttk.Label(answer_frame, style="TLabel")
label_situaltion.pack(anchor='w')
label_x = ttk.Label(answer_frame, style="Math.TLabel")
label_x.pack(anchor='w')
label_y = ttk.Label(answer_frame, style="Math.TLabel")
label_y.pack(anchor='w')

answer_frame.place(relwidth=0.2, relheight=1, relx=0.8)

info_frame.place(relwidth=1, relheight=0.8)



input_frame1 = ttk.Frame(root, style="TFrame")

label1 = ttk.Label(input_frame1, text="方程式1", style="TLabel")
label1.pack(anchor='w', side='left')
input1 = ttk.Entry(input_frame1, style="TEntry", font=math_font)
input1.pack(anchor='w', side='left', padx=10, fill='both', expand=1)

input_frame1.place(anchor='w', relwidth=0.8, relheight=0.09, rely=0.85)




input_frame2 = ttk.Frame(root, style="TFrame")

label2 = ttk.Label(input_frame2, text="方程式2", style="TLabel")
label2.pack(anchor='w', side='left')
input2 = ttk.Entry(input_frame2, style="TEntry", font=math_font)
input2.pack(anchor='w', side='left', padx=10, fill='both', expand=1)

input_frame2.place(anchor='w', relwidth=0.8, relheight=0.09, rely=0.95)




calc_btn = ttk.Button(root, text="計算",command=calc, style="TButton")
calc_btn.place(relwidth=0.2, relheight=0.2, relx=0.8, rely=0.8)

root.bind('<Configure>', resize)
root.mainloop()