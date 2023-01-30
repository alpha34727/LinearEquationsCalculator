import math
from tkinter import ttk, Tk
from tkextrafont import Font

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
        print(size)

def simply(x, y):
    if int(str(x/y).split('.')[1]) > 0:
        if len(str(y).split('.')[1]) > len(str(x).split('.')[1]):
            x, y = y, x

        nx = len(str(x).split('.')[1])
        x *= 10**nx
        y *= 10**nx
        gcd_xy = math.gcd(int(abs(x)), int(abs(y)))
        return f'{int(x)//gcd_xy}/{int(y)//gcd_xy}'
    else:
        return float(x/y)

def calc():
    raw1 = input1.get().lower()
    s1 = raw1.split('=')

    a1 = float(s1[0].split('x')[0])
    b1 = float(s1[0].split('x')[1].split('y')[0])
    c1 = float(s1[1])

    raw2 = input2.get().lower()
    s1 = raw2.split('=')

    a2 = float(s1[0].split('x')[0])
    b2 = float(s1[0].split('x')[1].split('y')[0])
    c2 = float(s1[1])

    d = a1 * b2 - a2 * b1
    dx = c1 * b2 - c2 * b1
    dy = a1 * c2 - a2 * c1

    label_d['text'] = f'Δ = {d}'
    label_dx['text'] = f'Δx = {dx}'
    label_dy['text'] = f'Δy = {dy}'

    if d == 0:
        label_x['text'] = 'x = nan'
        label_y['text'] = 'y = nan'
        if dx == 0 and dy == 0:
            label_situaltion['text'] = '無限多組解'
        else:
            label_situaltion['text'] = '無解'
    else:
        label_situaltion['text'] = '洽有一組解'
        label_x['text'] = f'x = {simply(dx, d)}'
        label_y['text'] = f'y = {simply(dy, d)}'

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







