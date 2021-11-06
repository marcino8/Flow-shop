import time

import numpy as np
import copy
from numpy import genfromtxt
import matplotlib.pyplot as plt


def initrandomswap_m(m):
    """
        :param m:
            np matrix obj, to randomly swap its rows
        :return:
            np matrix obj, with randomly swapped rows 5000 times
    """
    m2 = copy.copy(m)
    for i in range(1, 5000):
        m2 = randomswap_m(m2)
    return m2


def initrandomswap_max(m):
    """
    :return:
        np matrix obj, that has time calculated by calculate_time_matrices()
        lesser then 12300
    """
    m2 = copy.copy(m)
    while calculate_time_matrices(m2) > 12300:
        m2 = randomswap_m(m2)
    return m2


def randomswap_m(m2):
    """
        :param m2:
            np matrix obj, matrix to swap 2 random rows
        :return:
            np matrix obj, m2 with swapped two random rows
    """
    m = copy.copy(m2)
    where_to_put, what_to_put = generate_swap_indexes_m(m)
    m[[where_to_put, what_to_put]] = m[[what_to_put, where_to_put]]
    return m


def generate_swap_indexes_m(m):
    """
        :param m:
            obj to get ist lengths
        :return:
            List of 2 ints, being 2 random integer numbers from 0 to length of m exclusive
    """
    return [np.random.randint(1, len(m)), np.random.randint(1, len(m))]


def ihc(outside_iter, indide_iter, no_change_number, file_to_read, file_to_save):
    """
    :param outside_iter:
        int, number of outside iter
    :param indide_iter:
        int, number of inside iter
    :param no_change_number:
        int, after how many iterations without change of result should the loop break
    :param file_to_read:
        string, directory to read from
    :param file_to_save:
        string, directory to save to
    :return:
         Saves matrix calculated by IHC algorithm
    """
    m = genfromtxt(file_to_read, delimiter=',')
    m = m[1:][:]
    print(calculate_time_matrices(m))
    best_solution = initrandomswap_m(m)
    print(calculate_time_matrices(best_solution))
    times = []
    for j in range(1, outside_iter):
        start = time.time()
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
        tm = calculate_time_matrices(best_solution)
        print(tm)
        times.append(tm)
        print("time per outside iter :", time.time() - start)
    np.savetxt(file_to_save, best_solution, delimiter=",")
    print("FINAL FOR ", indide_iter, "INSIDE ITER ", outside_iter, "OUTSIDE ITER ", "WITH NO CHANGE ", no_change_number,
          "SAVED TO ", file_to_save)
    plt.plot(times)
    plt.ylabel("czas")
    save = file_to_save + ".jpeg"
    plt.savefig(save)


def calculate_time_matrices(matrix):
    """
        :param matrix:
            np matrix object
        :return:
            calculated time for given tasks positioning in flow shop problem
    """
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


