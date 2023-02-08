import math

def Sum(arr):
    """回傳List中所有分數的加總"""

    #計算分母的最小公倍數
    denominators = []
    for i in range(len(arr)):
        denominators.append(arr[i][1])
    denominators_lcm = math.lcm(*denominators)

    #擴分
    for i in range(len(arr)):
        arr[i][0] *= denominators_lcm // arr[i][1]
        arr[i][1] *= denominators_lcm // arr[i][1]

    #加總分子
    numerator = 0 #設定分子總和的初始值為0
    denominator = arr[0][1] #設定分母總和的初始值為擴分過後的分母值
    for i in range(len(arr)):
        numerator += arr[i][0]

    return [numerator, denominator]

def subtract(a, b):
    """回傳 分數a - 分數b 的值"""

    #計算分母的最小公倍數
    denominators_lcm = math.lcm(abs(a[1]), abs(b[1]))

    #擴分
    a[0] *= denominators_lcm // abs(a[1])
    a[1] *= denominators_lcm // abs(a[1])
    b[0] *= denominators_lcm // abs(b[1])
    b[1] *= denominators_lcm // abs(b[1])

    #相減並回傳
    return [a[0]-b[0], a[1]]

def add(a, b):
    """回傳 分數a + 分數b 的值"""

    #計算分母的最小公倍數
    denominators_lcm = math.lcm(abs(a[1]), abs(b[1]))

    #擴分
    a[0] *= denominators_lcm // abs(a[1])
    a[1] *= denominators_lcm // abs(a[1])
    b[0] *= denominators_lcm // abs(b[1])
    b[1] *= denominators_lcm // abs(b[1])

    #相加並回傳
    return [a[0]+b[0], a[1]]

def mutiply(a, b):
    """回傳 分數a * 分數b 的值"""
    return [a[0]*b[0], a[1]*b[1]]

def divide(a, b):
    """回傳 分數a / 分數b 的值"""
    return [a[0]*b[1], a[1]*b[0]]

def simply(arr):
    """回傳 化為最簡的分數"""
    a, b = arr[0], arr[1]

    #如果分母=0，回傳nan
    if b == 0:
        return [a, math.nan]

    #如果 (分子 / 分母) 的小數部分 > 0
    if int(str(a/b).split('.')[1]) > 0: 
        #約分
        gcd_ab = math.gcd(int(abs(a)), int(abs(b)))
        if b < 0: #使分母的值恆正
            a = -a
            b = -b
        return [a//gcd_ab, b//gcd_ab]
    else: #否則直接將 分子 / 分母，不必計算其最大公因數
        return [int(a/b), 1]

def simply_to_str(arr):
    """以字串形式回傳 化為最簡的分數"""
    a, b = arr[0], arr[1]

    #如果分母=0，回傳nan
    if b == 0:
        return str(math.nan)

    if b < 0: #使分母的值恆正
        a = -a
        b = -b

    #如果 (分子 / 分母) 的小數部分 > 0
    if int(str(a/b).split('.')[1]) > 0:
        #約分
        gcd_ab = math.gcd(int(abs(a)), int(abs(b)))
        return f'{a//gcd_ab}/{b//gcd_ab}'
    else: #否則直接將 分子 / 分母，不必計算其最大公因數
        return str(a/b)

def simply_to_numerical(arr):
    """以數值形式回傳 化為最簡的分數"""
    a, b = arr[0], arr[1]

    #如果分母=0，回傳nan
    if b == 0:
        return math.nan

    return a/b