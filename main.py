import tkinter as tk

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


    print(a1, b1, c1)
    print(a2, b2, c2)

    label_d['text'] = f'Δ = {d}'
    label_dx['text'] = f'Δx = {dx}'
    label_dy['text'] = f'Δy = {dy}'
    print(d, dx, dy)

    if d == 0:
        label_x['text'] = 'x = nan'
        label_y['text'] = 'y = nan'
        if dx == 0 and dy == 0:
            label_situaltion['text'] = '無限多組解'
            print('無限多組解')
        else:
            label_situaltion['text'] = '無解'
            print('無解')
    else:
        label_situaltion['text'] = '洽有一組解'
        label_x['text'] = f'x = {dx/d}'
        label_y['text'] = f'y = {dy/d}'
        print(f'x = {dx/d}')
        print(f'y = {dy/d}')

root = tk.Tk()
root.title("二元一次方程式計算機")
root.geometry("640x480")



info_frame = tk.Frame(root)

graph_frame = tk.Frame(info_frame)
graph_frame.place(relwidth=0.8, relheight=1)

answer_frame = tk.Frame(info_frame)

label_d = tk.Label(answer_frame, font=('Cambria', 16))
label_d.pack(anchor='w')
label_dx = tk.Label(answer_frame, font=('Cambria', 16))
label_dx.pack(anchor='w')
label_dy = tk.Label(answer_frame, font=('Cambria', 16))
label_dy.pack(anchor='w')
label_situaltion = tk.Label(answer_frame, font=('Cambria', 16))
label_situaltion.pack(anchor='w')
label_x = tk.Label(answer_frame, font=('Cambria', 16))
label_x.pack(anchor='w')
label_y = tk.Label(answer_frame, font=('Cambria', 16))
label_y.pack(anchor='w')


answer_frame.place(relwidth=0.2, relheight=1, relx=0.8)

info_frame.place(relwidth=1, relheight=0.8)



input_frame1 = tk.Frame(root)

label1 = tk.Label(input_frame1, text="方程式1", font=('微軟正黑體', 16))
label1.grid(row=0, column=0)
input1 = tk.Entry(input_frame1, font=('Cambria', 16))
input1.grid(row=0, column=1)

input_frame1.place(relwidth=0.8, relheight=0.1, rely=0.8)




input_frame2 = tk.Frame(root)

label2 = tk.Label(input_frame2, text="方程式2", font=('微軟正黑體', 16))
label2.grid(row=0, column=0)
input2 = tk.Entry(input_frame2, font=('Cambria', 16))
input2.grid(row=0, column=1)

input_frame2.place(relwidth=0.8, relheight=0.1, rely=0.9)




calc_btn = tk.Button(root, text="計算",command=calc, font=('微軟正黑體', 16))
calc_btn.place(relwidth=0.2, relheight=0.2, relx=0.8, rely=0.8)

root.mainloop()







