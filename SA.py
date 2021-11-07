import copy
import time
from numpy import genfromtxt
import numpy as np
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
    for i in range(1, 5000):
        m2 = randomswap_m2(m2)
    for i in range(1, 5000):
        m2 = randomswap_m3(m2)
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


def randomswap_m2(m2):
    """
    :param m2:
        np matrix obj, matrix to swap 2 random rows
    :return:
        np matrix obj, m2 with swapped two random rows
    """
    m = copy.copy(m2)
    x, y = 0, 0
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
    rnd = np.random.randint(4,22)
    interval = np.random.randint(2, rnd)
    middle = np.random.randint(interval, len(m) - interval - 1)
    temp = copy.copy(m[(middle - interval):middle, :])
    m[(middle - interval):middle, :] = m[(middle + 1):(interval + middle + 1), :]
    m[(middle + 1):(interval + middle + 1), :] = temp
    return m


def generate_swap_indexes_m(m):
    """
    :param m:
        obj to get ist lengths
    :return:
        List of 2 ints, being 2 random integer numbers from 0 to length of m exclusive
    """
    return [np.random.randint(0, len(m)), np.random.randint(0, len(m))]


def sa(start_T, red_T, geom, inside_iter, no_change_number, file_to_read, file_to_save):
    """
    :param start_T:
        float, start temperature
    :param red_T:
        float, number to reduce T every outside loop
    :param geom:
        bool, if true, temperature reduction is given as: t = t / (1 + red_T * t)
        if false emperature reduction is given as: t = t * red_T
    :param inside_iter:
        int, number of inside iterations
    :param no_change_number:
        int, after how many iterations without change of result should the loop break
    :param file_to_read:
        string, directory to read from
    :param file_to_save:
        string, directory to save to
    :return:
        Saves matrix calculated by SA algorithm
    """
    m = genfromtxt(file_to_read, delimiter=',')
    #m = m[1:][:]
    print(calculate_time_matrices(m))
    t = start_T
    solution = initrandomswap_m(m)
    solution = m
    times = []
    while t > 0.00001:
        start = time.time()
        tm = calculate_time_matrices(solution)
        print("TEMPERATURE", t, tm)
        no_change = 0
        times.append(tm)
        for i in range(1, inside_iter):
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
            elif np.random.random() < np.exp((-1) * delta_time / t):
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



# sample use
sa(1, 0.9, False, 20000, 10009, "dane2_sa_STERIDES.csv", 'dane2_bbs.csv')


