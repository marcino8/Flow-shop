import copy
from numpy import genfromtxt
import numpy as np


def initrandomswap_m(m):
    m2 = copy.copy(m)
    for i in range(1, 5000):
        randomswap_m(m2)
    return m2



def randomswap_m(mt):
    m=copy.copy(mt)
    where_to_put, what_to_put = generate_swap_indexes_m(m)
    temp = m[where_to_put]
    m[where_to_put] = m[what_to_put]
    m[what_to_put] = temp
    return m



def generate_swap_indexes_m(m):
    return [np.random.randint(1, len(m)), np.random.randint(1, len(m))]


def sa(m):
    t = 0.99
    solution = initrandomswap_m(m)
    while t > 0.000000001:
        print(t, calculate_time_matrices(solution))
        no_change = 0
        for i in range(1, 30000):
            m2 = randomswap_m(solution)
            t1 = calculate_time_matrices(solution)
            t2 = calculate_time_matrices(m2)
            delta_time = t2 - t1
            if delta_time < 0:
                solution = m2
            elif np.random.random() > np.exp(delta_time / t):
                solution = m2
            else:
                no_change+=1
            if no_change>5000:
                break
        t = t * 0.9
    return solution


def calculate_time_matrices(matrix):
    m = copy.copy(matrix[:, 1:])
    for row in range(0, len(m)):
        for el in range(0, len(m[0])):
            if row == 0 and el == 0:
                pass
            elif row == 0:
                m[row][el] += m[row, el - 1]
            elif el == 0:
                m[row][el] += m[row - 1][el]
            else:
                m[row][el] += max(m[row - 1][el], m[row][el - 1])
    return m[len(m) - 1][len(m[0]) - 1]


def load():
    df = genfromtxt('dane2.csv', delimiter=',')
    df = df[1:][:]
    final = sa(df)
    np.savetxt("dane2_sa099_092.csv", final, delimiter=",")
    print(calculate_time_matrices(final))


load()