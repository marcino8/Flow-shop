import copy
import time

from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt


def initrandomswap_m(m):
    m2 = copy.copy(m)
    for i in range(1, 5000):
        m2=randomswap_m(m2)
    return m2


def randomswap_m(m2):
    m=copy.copy(m2)
    where_to_put, what_to_put = generate_swap_indexes_m(m)
    m[[where_to_put,what_to_put]] = m[[what_to_put,where_to_put]]
    return m


def generate_swap_indexes_m(m):
    return [np.random.randint(1, len(m)), np.random.randint(1, len(m))]


def sa(start_T, red_T, geom, inside_iter, no_change_number, file_to_read, file_to_save):
    m = genfromtxt(file_to_read, delimiter=',')
    m = m[1:][:]
    t = start_T
    solution = initrandomswap_m(m)
    times=[]
    while t > 0.0001:
        start = time.time()
        tm = calculate_time_matrices(solution)
        print("TEMPERATURE", t, tm )
        no_change = 0
        times.append(tm)
        for i in range(1, inside_iter):
            m2 = randomswap_m(solution)
            t1 = calculate_time_matrices(solution)
            t2 = calculate_time_matrices(m2)
            delta_time = t2 - t1
            if delta_time < 0:
                solution = m2
            elif np.random.random() > np.exp((-1)*delta_time / t):
                solution = m2
            else:
                no_change += 1
            if no_change > no_change_number:
                break
        print("time per outside iter :", time.time() - start)
        if geom:
            t = t / (1 + red_T * t)
        else:
            t = t * red_T

    np.savetxt(file_to_save, solution, delimiter=",")
    print("FINAL FOR ", t, "T START ", inside_iter, "INSIDE ITERATIONS ", red_T, "REDUCTION ", "SAVED TO ",
          file_to_save)
    plt.plot(times)
    plt.ylabel("czas")
    plt.show()
    save = file_to_save + ".jpeg"
    plt.savefig(save)


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

sa(0.9, 0.3, True, 10000, 999999, 'dane2.csv', 'dane2_sa_09_geom03_nonochange.csv')

