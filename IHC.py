import time

import numpy as np
import copy
from numpy import genfromtxt


def initrandomswap_m(m):
    m2 = copy.copy(m)
    for i in range(1, 5000):
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


def ihc(outside_iter, indide_iter, no_change_number, file_to_read, file_to_save):
    m = genfromtxt(file_to_read, delimiter=',')
    m = m[1:][:]
    best_solution = initrandomswap_m(m)
    for j in range(1, outside_iter):
        start=time.time()
        print("OUTSIDE ITER:", j)
        solution = initrandomswap_m(m)
        no_change = 0
        for i in range(1, indide_iter):
            m2 = randomswap_m(solution)
            t1 = calculate_time_matrices(solution)
            t2 = calculate_time_matrices(m2)
            delta_time = t2 - t1
            if delta_time < 0:
                solution = m2
            else:
                no_change += 1
            if no_change > no_change_number:
                break
        if calculate_time_matrices(best_solution) - calculate_time_matrices(solution) > 0:
            best_solution = solution
        print(calculate_time_matrices(best_solution))
        print("time per outside iter :", time.time() - start)
    np.savetxt(file_to_save, best_solution, delimiter=",")
    print("FINAL FOR ", indide_iter, "INSIDE ITER ", outside_iter, "OUTSIDE ITER ", "WITH NO CHANGE ", no_change_number, "SAVED TO ", file_to_save)


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


ihc(100, 1000, 999999, 'dane2.csv', 'dane2_ihc_100_1k_nonochange') # FOR NOT USING NO_CHANGE PLEASE PUT BIG NUMBER


