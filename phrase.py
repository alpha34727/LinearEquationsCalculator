import re
import math
from decimal import *
from fraction_calc import *

def phrase_equation(equation):
    space_pattern = re.compile(r"\s+")
    equation = re.sub(space_pattern, '', equation)
    equation = equation.lower()

    left = equation.split('=')[0]
    right = equation.split('=')[1]

    x_pattern = re.compile(r"(-?\d*[.]?\d*?)/?(-?\d*[.]?\d*?)?x")
    y_pattern = re.compile(r"(-?\d*[.]?\d*?)/?(-?\d*[.]?\d*?)?y")
    not_const_pattern = re.compile(r"[-+]?\d*[.]?\d*?/?[-]?\d*[.]?\d*?[xy]")

    def fraction_to_list(arr):
        if len(arr) <= 0:
            return [[0, 1]]
        result = []
        for i in arr:
            i = list(i)
            if i[1] == '':
                i[1] = '1.0'
            if '.' not in i[0]:
                i[0]+='.0'
            if '.' not in i[1]:
                i[1]+='.0'
            if i[1].startswith('-'):
                if i[0].startswith('-'):
                    i[0] = i[0].split('-')[1]
                    i[1] = i[1].split('-')[1]
                else:
                    i[0] = '-' + i[0]
                    i[1] = i[1].split('-')[1]
            float_point = max(len(i[0].split('.')[1]), len(i[1].split('.')[1]))
            i[0] = int(Decimal(i[0]) * (10**float_point))
            i[1] = int(Decimal(i[1]) * (10**float_point))
            result.append(i)
        return result

    left_x = Sum(fraction_to_list(re.findall(x_pattern, left)))
    right_x = Sum(fraction_to_list(re.findall(x_pattern, right)))
    subtracted_x = subtract(left_x, right_x)
    subtracted_x = simply(subtracted_x)

    left_y = Sum(fraction_to_list(re.findall(y_pattern, left)))
    right_y = Sum(fraction_to_list(re.findall(y_pattern, right)))
    subtracted_y = subtract(left_y, right_y)
    subtracted_y = simply(subtracted_y)

    def const_phrase(left, right):
        not_const_left = ""
        for i in re.finditer(not_const_pattern, left):
            not_const_left += i.group()

        not_const_right = ""
        for i in re.finditer(not_const_pattern, right):
            not_const_right += i.group()

        right_const = ''
        if not_const_right != '' and not_const_right in right:
            for i in right.split(not_const_right):
                right_const += i
        else:
            right_const = right

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
        


        left_const = ''
        if not_const_left != '' and not_const_left in left:
            for i in left.split(not_const_left):
                left_const += i
        else:
            left_const = left

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

        

        return left_const, right_const

    left_const, right_const = const_phrase(left, right)

    left_const = Sum(fraction_to_list(left_const))
    right_const = Sum(fraction_to_list(right_const))
    subtracted_const = subtract(right_const, left_const)
    subtracted_const = simply(subtracted_const)

    return subtracted_x, subtracted_y, subtracted_const