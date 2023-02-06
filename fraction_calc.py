import math

def Sum(arr):
    denominators = []
    for i in range(len(arr)):
        denominators.append(arr[i][1])
    denominators_lcm = math.lcm(*denominators)
    for i in range(len(arr)):
        arr[i][0] *= denominators_lcm // arr[i][1]
        arr[i][1] *= denominators_lcm // arr[i][1]

    numerator = 0
    
    denominator = arr[0][1]
    for i in range(len(arr)):
        numerator += arr[i][0]

    return [numerator, denominator]

def subtract(a, b):
    denominators_lcm = math.lcm(abs(a[1]), abs(b[1]))
    a[0] *= denominators_lcm // abs(a[1])
    a[1] *= denominators_lcm // abs(a[1])
    b[0] *= denominators_lcm // abs(b[1])
    b[1] *= denominators_lcm // abs(b[1])
    return [a[0]-b[0], a[1]]

def add(a, b):
    denominators_lcm = math.lcm(abs(a[1]), abs(b[1]))
    a[0] *= denominators_lcm // abs(a[1])
    a[1] *= denominators_lcm // abs(a[1])
    b[0] *= denominators_lcm // abs(b[1])
    b[1] *= denominators_lcm // abs(b[1])
    return [a[0]+b[0], a[1]]

def mutiply(a, b):
    return [a[0]*b[0], a[1]*b[1]]

def divide(a, b):
    return [a[0]*b[1], a[1]*b[0]]

def simply(arr):
    a, b = arr[0], arr[1]
    if b == 0:
        return [a, math.nan]
    if int(str(a/b).split('.')[1]) > 0:
        gcd_ab = math.gcd(int(abs(a)), int(abs(b)))
        if b < 0:
            a = -a
            b = -b
        return [a//gcd_ab, b//gcd_ab]
    else:
        return [int(a/b), 1]

def simply_to_str(arr):
    a, b = arr[0], arr[1]
    if b == 0:
        return str(math.nan)
    if b < 0:
        a = -a
        b = -b
    if int(str(a/b).split('.')[1]) > 0:
        gcd_ab = math.gcd(int(abs(a)), int(abs(b)))
        return f'{a//gcd_ab}/{b//gcd_ab}'
    else:
        return str(a/b)

def simply_to_numerical(arr):
    a, b = arr[0], arr[1]
    if b == 0:
        return math.nan
    return a/b