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

#將原始matplotlib中的工具列的元件從tk轉換成ttk，基於matplotlib的原始碼修改
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

#預設的視窗長與寬
root_width = 800 #寬
root_height = 480 #長

def resize(event):
    """根據視窗大小改變介面的文字大小"""

    #如果發生Configure的元件是視窗
    if str(event.widget) == '.':
        #指定使用全域變數
        global root_width
        global root_height

        #如果尺寸改變
        if event.width != root_width or event.height != root_height:
            root_width = event.width #將寬度更新
            root_height = event.height #將高度更新

            #指定使用全域變數
            global default_font
            global math_font

            #計算字體大小
            size = int(event.width*event.height/32000 + 4)
            if size > 28:
                size = 28
            elif size < 12:
                size = 12
            
            #改變字體大小
            default_font.config(size=size)
            math_font.config(size=size)

def calc():
    """計算二元一次方程組的解，並繪製圖形"""

    #清除圖形
    line.clear()

    #設定垂直軸與水平軸的名稱
    line.set_xlabel("x", loc='right')
    line.set_ylabel("y", loc='top')

    #解析輸入的方程式，並儲存至a1, b1, c1
    #a1 = x項，b1 = y項，c1 = 常數項
    a1, b1, c1 = phrase_equation(input1.get())
    a2, b2, c2 = phrase_equation(input2.get())

    #克拉瑪公式計算
    d = subtract(mutiply(a1, b2), mutiply(a2, b1))  #Δ = a1 * b2 - a2 * b1
    dx = subtract(mutiply(c1, b2), mutiply(c2, b1)) #Δx = c1 * b2 - c2 * b1
    dy = subtract(mutiply(a1, c2), mutiply(a2, c1)) #Δy = a1 * c2 - a2 * c1
    
    #顯示 Δ, Δx, Δy 的結果
    label_d['text'] = f'Δ = {simply_to_str(d)}'
    label_dx['text'] = f'Δx = {simply_to_str(dx)}'
    label_dy['text'] = f'Δy = {simply_to_str(dy)}'

    #繪製x軸與y軸
    line.axhline(y=0, color="#000000")
    line.axvline(x=0, color="#000000")

    #預設x = nan, y = nan
    x = math.nan
    y = math.nan

    #預設x與y顯示的結果為 ""
    x_str = ""
    y_str = ""

    """
    克拉瑪公式：
    
    如果Δ != 0，則此方程組洽有一組解，其解為 x = Δx / Δ, y = Δy / Δ
    如果Δ = Δx = Δy = 0，則此方程組有無限多組解
    如果Δ = 0, Δx or Δy 有一!=0，則此方程組無解
    """
    if d[0] == 0:
        if dx[0] == 0 and dy[0] == 0:
            #有無限多組解的情況
            label_situaltion['text'] = '無限多組解'
        else:
            #無解的情況
            label_situaltion['text'] = '無解'

        #計算 方程式1 與 x=0 的交點 和 方程式1 與 x=1 的交點，並在兩點間繪製一條直線
        line.axline((0, simply_to_numerical(divide(c1, b1))), (1, simply_to_numerical(divide(subtract(c1, a1), b1))), color="#4fc3f7", label=input1.get())

        #計算 方程式2 與 x=0 的交點 和 方程式2 與 x=1 的交點，並在兩點間繪製一條直線
        line.axline((0, simply_to_numerical(divide(c2, b2))), (1, simply_to_numerical(divide(subtract(c2, a2), b2))), color="#ffb74d", label=input2.get())
        line.grid(which='major')
    else:
        #洽有一組解的情況
        label_situaltion['text'] = '洽有一組解'

        x = divide(dx, d) #計算x = Δx / Δ
        y = divide(dy, d) #計算y = Δy / Δ
        x_str = simply_to_str(x) #化簡x，並儲存至顯示x結果的字串
        y_str = simply_to_str(y) #化簡y，並儲存至顯示y結果的字串

        #計算 方程式1 與 x=0 的交點 和 方程式1 與 y=0 的交點，並在兩點間繪製一條直線
        line.axline((0, simply_to_numerical(divide(c1, b1))), (simply_to_numerical(divide(c1, a1)), 0), color="#4fc3f7", label=input1.get())

        #計算 方程式2 與 x=0 的交點 和 方程式2 與 y=0 的交點，並在兩點間繪製一條直線
        line.axline((0, simply_to_numerical(divide(c2, b2))), (simply_to_numerical(divide(c2, a2)), 0), color="#ffb74d", label=input2.get())
        line.grid(which='major')

        #繪製兩方程組的解
        line.plot(simply_to_numerical(x), simply_to_numerical(y), 'o', color="#ef5350")
    
    #顯示x和y的解
    label_x['text'] = f'x = {x_str}'
    label_y['text'] = f'y = {y_str}'

    #顯示圖例
    labels = [input1.get(), input2.get()]
    handles, _ = line.get_legend_handles_labels()
    line.legend(handles = handles, labels = labels, loc='upper right')

    #改變x軸與y軸每格的距離為1
    line.xaxis.set_major_locator(MultipleLocator(1))
    line.yaxis.set_major_locator(MultipleLocator(1))
    
    #繪製圖形
    canvas.draw()

root = Tk()
root.title("二元一次方程式計算機") #視窗標題
root.geometry(f"{root_width}x{root_height}") #設定視窗大小
root.config(background="#FFFFFF", padx=10, pady=10) #設定視窗背景

#字體設定
default_font = Font(file="./font/NotoSansTC-Regular.otf", family="Noto Sans TC", size=16)
math_font = Font(file="./font/STIXTwoText-Medium.otf", family="STIX Two Text Medium", size=16)

#風格設定
style = ttk.Style()
style.configure("TFrame", background="#FFFFFF")
style.configure("TCheckbutton", background="#FFFFFF")
style.configure("TLabel", background="#FFFFFF", font=default_font)
style.configure("Toolbar.TLabel", background="#FFFFFF", font=Font(family="STIX Two Text Medium", size=64))
style.configure("TButton", background="#FFFFFF", font=default_font)
style.configure("Math.TLabel", background="#FFFFFF", font=math_font)
style.configure("Math.TButton", background="#FFFFFF", font=math_font)
style.configure("TEntry", background="#FFFFFF")

#顯示結果的Frame
info_frame = ttk.Frame(root, style="TFrame")

#顯示圖形的Frame
graph_frame = ttk.Frame(info_frame, style="TFrame")

#圖形與工具列設定
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

#顯示解的Frame
answer_frame = ttk.Frame(info_frame, style="TFrame")

#標籤設定
label_d = ttk.Label(answer_frame, style="Math.TLabel") #顯示Δ的標籤
label_d.pack(anchor='w')
label_dx = ttk.Label(answer_frame, style="Math.TLabel") #顯示Δx的標籤
label_dx.pack(anchor='w')
label_dy = ttk.Label(answer_frame, style="Math.TLabel") #顯示Δy的標籤
label_dy.pack(anchor='w')
label_situaltion = ttk.Label(answer_frame, style="TLabel") #顯示方程組解的結果的標籤
label_situaltion.pack(anchor='w')
label_x = ttk.Label(answer_frame, style="Math.TLabel") #顯示x的標籤
label_x.pack(anchor='w')
label_y = ttk.Label(answer_frame, style="Math.TLabel") #顯示y的標籤
label_y.pack(anchor='w')

answer_frame.place(relwidth=0.2, relheight=1, relx=0.8)

info_frame.place(relwidth=1, relheight=0.8)


#方程組1輸入框的Frame
input_frame1 = ttk.Frame(root, style="TFrame")

#輸入框設定
label1 = ttk.Label(input_frame1, text="方程式1", style="TLabel") #顯示 標籤名 的標籤
label1.pack(anchor='w', side='left')
input1 = ttk.Entry(input_frame1, style="TEntry", font=math_font) #輸入框
input1.pack(anchor='w', side='left', padx=10, fill='both', expand=1)

input_frame1.place(anchor='w', relwidth=0.8, relheight=0.09, rely=0.85)

#方程組2輸入框的Frame
input_frame2 = ttk.Frame(root, style="TFrame")

#輸入框設定
label2 = ttk.Label(input_frame2, text="方程式2", style="TLabel") #顯示 標籤名 的標籤
label2.pack(anchor='w', side='left')
input2 = ttk.Entry(input_frame2, style="TEntry", font=math_font) #輸入框
input2.pack(anchor='w', side='left', padx=10, fill='both', expand=1)

input_frame2.place(anchor='w', relwidth=0.8, relheight=0.09, rely=0.95)

#計算按鈕
calc_btn = ttk.Button(root, text="計算",command=calc, style="TButton")
calc_btn.place(relwidth=0.2, relheight=0.2, relx=0.8, rely=0.8)

root.bind('<Configure>', resize)
root.mainloop()