import math
from tkinter import ttk, Tk
from tkextrafont import Font
from phrase import phrase_equation
from fraction_calc import *

def resize(event):
    if str(event.widget) == '.':
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
    a1, b1, c1 = phrase_equation(input1.get())
    a2, b2, c2 = phrase_equation(input2.get())

    d = subtract(mutiply(a1, b2), mutiply(a2, b1))
    dx = subtract(mutiply(c1, b2), mutiply(c2, b1))
    dy = subtract(mutiply(a1, c2), mutiply(a2, c1))

    label_d['text'] = f'Δ = {d[0]/d[1]}'
    label_dx['text'] = f'Δx = {dx[0]/dx[1]}'
    label_dy['text'] = f'Δy = {dy[0]/dy[1]}'

    x = math.nan
    y = math.nan

    if d[0] == 0:
        if dx[0] == 0 and dy[0] == 0:
            label_situaltion['text'] = '無限多組解'
        else:
            label_situaltion['text'] = '無解'
    else:
        label_situaltion['text'] = '洽有一組解'
        x = simply_to_str(divide(dx, d))
        y = simply_to_str(divide(dy, d))

    label_x['text'] = f'x = {x}'
    label_y['text'] = f'y = {y}'

root = Tk()
root.title("二元一次方程式計算機")
root.geometry(f"800x480")
root.config(background="#FFFFFF", padx=10, pady=10)

default_font = Font(file="./font/NotoSansTC-Regular.otf", family="Noto Sans TC", size=16)
math_font = Font(file="./font/STIXTwoText-Medium.otf", family="STIX Two Text Medium", size=16)

style = ttk.Style()
style.configure("TFrame", background="#FFFFFF")
style.configure("TLabel", background="#FFFFFF", font=default_font)
style.configure("TButton", background="#FFFFFF", font=default_font)
style.configure("Math.TLabel", background="#FFFFFF", font=math_font)
style.configure("Math.TButton", background="#FFFFFF", font=math_font)
style.configure("TEntry", background="#FFFFFF")

info_frame = ttk.Frame(root, style="TFrame")

graph_frame = ttk.Frame(info_frame, style="TFrame")
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







