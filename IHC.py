import numpy as np
import copy
from numpy import genfromtxt


def initrandomswap_m(m):
    m2=copy.copy(m)
    for i in range(1,300):
        randomswap_m(m2)
    return m2

def randomswap_m(mt):
    m = copy.copy(mt)
    where_to_put, what_to_put = generate_swap_indexes_m(m)
    temp = m[where_to_put]
    m[where_to_put] = m[what_to_put]
    m[what_to_put] = temp
    return m

def generate_swap_indexes_m(m):
    return [np.random.randint(1, len(m)), np.random.randint(1, len(m))]

def ihc(m):
    best_solution = initrandomswap_m(m)
    for j in range(1,100):
        print(j)
        solution = initrandomswap_m(m)
        for i in range(1, 10000):
            m2 = randomswap_m(solution)
            t1 = calculate_time_matrices(solution)
            t2 = calculate_time_matrices(m2)
            delta_time = t2 - t1
            if delta_time < 0:
                solution = m2
        if calculate_time_matrices(best_solution)-calculate_time_matrices(solution) > 0:
            best_solution = solution
        print(calculate_time_matrices(best_solution))
    return best_solution


def calculate_time_matrices(matrix):
    m=copy.copy(matrix[:,1:])
    for row in range(0, len(m)):
        for el in range(0, len(m[0])):
            if row == 0 and el == 0:
                pass
            elif row == 0:
                m[row][el] += m[row, el-1]
            elif el == 0:
                m[row][el] += m[row-1][el]
            else:
                m[row][el] += max(m[row-1][el], m[row][el-1])
    return m[len(m)-1][len(m[0])-1]

def load():
    df=genfromtxt('dane2.csv', delimiter=',')
    df=df[1:][:]
    final = ihc(df)
    final.to_csv("dane2_ihc.csv", sep=",")
    print(calculate_time_matrices(final))


df=genfromtxt('dane2.csv', delimiter=',')
df=df[1:,]
print(df)
print(calculate_time_matrices(df))
df=initrandomswap_m(df)
print(df)
print(calculate_time_matrices(df))

load()