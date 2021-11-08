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


def ihc(outside_iter, indide_iter, no_change_number, file_to_read, file_to_save, headers=False, init_swap=False):
    """
    :param init_swap:
        bool, if true, swaps loaded from file solution
    :param headers:
        bool, if true, deletes headers
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
    if headers:
        m = m[1:][:]
    if init_swap:
        best_solution = initrandomswap_m(m)
    else:
        best_solution = m
    print(calculate_time_matrices(m))
    print(calculate_time_matrices(best_solution))
    times = []
    times2 = []
    for j in range(0, outside_iter):
        start = time.time()
        print("OUTSIDE ITER:", j)
        solution = initrandomswap_m(m)
        no_change = 0
        for i in range(0, indide_iter):
            rnd = np.random.randint(1, 4)
            if rnd == 1:
                m2 = randomswap_m(solution)
            elif rnd == 2:
                m2 = randomswap_m2(solution)
            else:
                m2 = randomswap_m3(solution)
            t1 = calculate_time_matrices(solution)
            t2 = calculate_time_matrices(m2)
            delta_time = t2 - t1
            if delta_time < 0:
                solution = m2
            else:
                no_change += 1
            if no_change > no_change_number:
                break
        tm = calculate_time_matrices(best_solution)
        tm2 = calculate_time_matrices(solution)
        if tm - tm2 > 0:
            best_solution = solution
        print(tm)
        times.append(tm)
        times2.append(tm2)
        print("time per outside iter :", time.time() - start)
    np.savetxt(file_to_save, best_solution, delimiter=",")
    print("FINAL FOR ", indide_iter, "INSIDE ITER ", outside_iter, "OUTSIDE ITER ", "WITH NO CHANGE ", no_change_number,
          "SAVED TO ", file_to_save)
    ploted(
        x=np.linspace(1, outside_iter, outside_iter),
        y1=times,
        y2=times2,
        xlab="TIME",
        ylab="ITER",
        y1lab="pretender times for " + str(indide_iter) + " new iter",
        y2lab="best times for overall iter",
        title="IHC",
        savename=file_to_save)


def randomswap_m2(m2):
    """
    :param m2:
        np matrix obj, matrix to swap 2 random rows
    :return:
        np matrix obj, m2 with swapped two random rows
    """
    m = copy.copy(m2)
    where_to_put, what_to_put = generate_swap_indexes_m(m)
    if what_to_put >= where_to_put:
        x = where_to_put
        y = what_to_put
    else:
        x = what_to_put
        y = where_to_put
    reverse = m[x:y, :]
    reverse = np.flip(reverse, axis=0)
    m[x:y, :] = reverse
    return m


def randomswap_m3(m2):
    """
    :param m2:
        np matrix obj, matrix to swap 2 random rows
    :return:
        np matrix obj, m2 with swapped two random rows
    """
    m = copy.copy(m2)
    rnd = np.random.randint(4, 8)
    interval = np.random.randint(2, rnd)
    middle = np.random.randint(interval, len(m) - interval - 1)
    temp = copy.copy(m[(middle - interval):middle, :])
    m[(middle - interval):middle, :] = m[(middle + 1):(interval + middle + 1), :]
    m[(middle + 1):(interval + middle + 1), :] = temp
    return m


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


def ploted(x, y1, y2, ylab, xlab, y1lab, y2lab, title, savename):
    plt.plot(x, y1, label=y1lab)
    plt.plot(x, y2, label=y2lab)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.title(title)
    plt.legend()
    plt.savefig(savename + "wykres.jpeg")


ihc(outside_iter=100,
    indide_iter=20000,
    no_change_number=99999,
    file_to_read="dane3.csv",
    file_to_save="dane3ihc.csv",
    init_swap=True,
    headers=True)
