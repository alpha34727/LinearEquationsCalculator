raw1 = input().lower()
s1 = raw1.split('=')

a1 = float(s1[0].split('x')[0])
b1 = float(s1[0].split('x')[1].split('y')[0])
c1 = float(s1[1])

raw2 = input().lower()
s1 = raw2.split('=')

a2 = float(s1[0].split('x')[0])
b2 = float(s1[0].split('x')[1].split('y')[0])
c2 = float(s1[1])

d = a1 * b2 - a2 * b1
dx = c1 * b2 - c2 * b1
dy = a1 * c2 - a2 * c1

print(a1, b1, c1)
print(a2, b2, c2)

print(d, dx, dy)

if d == 0:
    if dx == 0 and dy == 0:
        print('無限多組解')
    else:
        print('無解')
else:
    print(f'x = {dx/d}')
    print(f'y = {dy/d}')
