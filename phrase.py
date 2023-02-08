import re
from decimal import *
from fraction_calc import *

def phrase_equation(equation):
    """輸入一方程式，回傳(x, y, 常數項)"""

    #利用RE去除空格
    space_pattern = re.compile(r"\s+")
    equation = re.sub(space_pattern, '', equation)
    equation = equation.lower() #確保輸入的x和y都是小寫

    #將方程式分割成左右式
    left = equation.split('=')[0]
    right = equation.split('=')[1]

    #RE的格式
    x_pattern = re.compile(r"(-?\d*[.]?\d*?)/?(-?\d*[.]?\d*?)?x") #x項
    y_pattern = re.compile(r"(-?\d*[.]?\d*?)/?(-?\d*[.]?\d*?)?y") #y項
    not_const_pattern = re.compile(r"[-+]?\d*[.]?\d*?/?[-]?\d*[.]?\d*?[xy]") #不是常數項

    def fraction_to_list(arr):
        """將輸入的List中 字串形式儲存的分數 轉為 數值形式儲存的分數，並讓分母分子的位數相同

           回傳整理好的分數
        """
        if len(arr) <= 0:
            return [[0, 1]]
        result = []
        for i in arr:
            i = list(i)
            if i[0] == '':
                i[0] = '1.0'
            if i[1] == '':
                i[1] = '1.0'
            if '.' not in i[0]:
                i[0]+='.0'
            if '.' not in i[1]:
                i[1]+='.0'
            if i[1].startswith('-'):
                i[0] = i[0].split('-')[1]
                i[1] = i[1].split('-')[1]
            float_point = max(len(i[0].split('.')[1]), len(i[1].split('.')[1]))
            i[0] = int(Decimal(i[0]) * (10**float_point))
            i[1] = int(Decimal(i[1]) * (10**float_point))
            result.append(i)
        return result

    left_x = Sum(fraction_to_list(re.findall(x_pattern, left))) #將左式的x總和
    right_x = Sum(fraction_to_list(re.findall(x_pattern, right))) #將右式的x總和
    subtracted_x = subtract(left_x, right_x) #將左式的x - 右式的x
    subtracted_x = simply(subtracted_x) #化簡x

    left_y = Sum(fraction_to_list(re.findall(y_pattern, left))) #將左式的y總和
    right_y = Sum(fraction_to_list(re.findall(y_pattern, right))) #將右式的y總和
    subtracted_y = subtract(left_y, right_y) #將右式的y - 左式的y
    subtracted_y = simply(subtracted_y) #化簡y

    #化簡常數項的函式
    def const_phrase(left, right):
        """輸入左式與右式，回傳(左式的常數項, 右式的常數項)
           
           步驟如下：
           1. 利用正則表達式篩選出左右式中不是常數項的字串
           2. 將原始的左右式-不是常數項的字串，得到左右式常數項的字串
           3. 將左右式常數項的字串依照 -, +, / 分割成List
        """

        #利用正則表達式篩選出左右式中不是常數項的字串
        not_const_left = ""
        for i in re.finditer(not_const_pattern, left):
            not_const_left += i.group()

        not_const_right = ""
        for i in re.finditer(not_const_pattern, right):
            not_const_right += i.group()

        #將原始的右式-右式中不是常數項的字串，得到右式常數項的字串
        right_const = ''
        if not_const_right != '' and not_const_right in right:
            for i in right.split(not_const_right):
                right_const += i
        else:
            right_const = right

        #將右式常數項的字串依照 -, +, / 分割成List
        right_const = right_const.split('-')
        for i in range(1, len(right_const)):
            right_const[i] = '-' + right_const[i]

        right_const_add = []
        for i in range(len(right_const)):
            if right_const[i] != '':
                right_const_add += right_const[i].split('+')
        right_const = right_const_add

        for i in range(len(right_const)):
            right_const_fraction = right_const[i].split('/')
            if len(right_const[i].split('/')) > 1:
                right_const[i] = right_const_fraction
            else:
                right_const[i] = [right_const_fraction[0], '1']
        

        #將原始的左式-左式中不是常數項的字串，得到左式常數項的字串
        left_const = ''
        if not_const_left != '' and not_const_left in left:
            for i in left.split(not_const_left):
                left_const += i
        else:
            left_const = left

        #將左式常數項的字串依照 -, +, / 分割成List
        left_const = left_const.split('-')
        for i in range(1, len(left_const)):
            left_const[i] = '-' + left_const[i]

        left_const_add = []
        for i in range(len(left_const)):
            if left_const[i] != '':
                left_const_add += left_const[i].split('+')
        left_const = left_const_add

        for i in range(len(left_const)):
            left_const_fraction = left_const[i].split('/')
            if len(left_const[i].split('/')) > 1:
                left_const[i] = left_const_fraction
            else:
                left_const[i] = [left_const_fraction[0], '1']

        #回傳結果
        return left_const, right_const

    #將左右式的常數項進行解析
    left_const, right_const = const_phrase(left, right)

    left_const = Sum(fraction_to_list(left_const)) #將左式的常數項相加
    right_const = Sum(fraction_to_list(right_const)) #將右式的常數項相加
    subtracted_const = subtract(right_const, left_const) #將左式的常數項 - 右式的常數項
    subtracted_const = simply(subtracted_const) #化簡常數項

    #回傳結果
    return subtracted_x, subtracted_y, subtracted_const