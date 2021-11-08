import time
import numpy as np
import copy
import matplotlib.pyplot as plt


def initrandomswap_m(m):
    """
    :param m:
        np matrix obj, to randomly swap its rows
    :return:
        np matrix obj, with randomly swapped rows 5000 times
    """
    m2 = copy.copy(m)
    for i in range(1, 500):
        m2 = randomswap_m(m2)
    return m2


def calculate_moves2(m, tl, zeros):
    """
    This is used to calculate every possible swap of 2 rows, and find the best swap
    :param zeros:
        bool, used to specify allowing zero time change swaps
    :param m:
        np matrix obj on which all possible swaps of 2 different rows will be made
    :param tl:
        np matrix obj, size len(m) x len(m), tabu list with blocked swaps
    :return:
        List of 3 ints, first and second are indexes of rows to swap to get best result in time save/loss
        third is how much time is saved/lost by this swap
    """
    move = [0, 0, 99999]
    for i in range(0, len(m)):
        for j in range(i + 1, len(m)):
            if is_not_present_in_tl(tl, i, j):
                m2 = swap(m, i, j)
                delta_time = calculate_time_matrices(m2) - calculate_time_matrices(m)
                if zeros:
                    if delta_time < move[2]:
                        move = [i, j, delta_time]
                else:
                    if delta_time < move[2] and delta_time != 0:
                        move = [i, j, delta_time]
    return move


def swap(mt, x, y):
    """
    :param mt:
        np matrix obj, matrix to swap rows
    :param x:
        int, row index to swap
    :param y:
        int, row index to swap
    :return:
        np matrix obj, with swapped x and y rows
    """
    m = copy.copy(mt)
    m[[x, y]] = m[[y, x]]
    return m


def randomswap_m(mt):
    """
    :param mt:
        np matrix obj, matrix to swap 2 random rows
    :return:
        np matrix obj, m2 with swapped two random rows
    """
    m = copy.copy(mt)
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
    return [np.random.randint(0, len(m)), np.random.randint(0, len(m))]


def is_not_present_in_tl(tl, i, j):
    """
    This method checks if the move about to be made is in tabu list (blocked moves list)
    :param tl:
        np matrix obj, tabu list
    :param i:
        int, row index to swap
    :param j:
        int, row index to swap
    :return:
        False if swap is prohibited by Tabu list
        True otherwise
    """
    return 0 == tl[i, j] and 0 == tl[j, i]


def update_tabu_list(tl):
    """
    Updates tabu list after iteration end
    """
    for i in range(0, len(tl)):
        for j in range(0, len(tl)):
            if tl[i][j] > 0:
                tl[i][j] -= 1
    return tl


def ts(s, inside_iter, file_to_read, file_to_save, allow_zeros=False, headers=False, init_swap=False):
    """
    :param allow_zeros:
        bool, if true, allows TS to make swaps that result in no change in overall time
    :param init_swap:
        bool, if true, swaps loaded from file solution
    :param headers:
        bool, if true, deletes headers
    :param s:
        int, how many iterations are swaps blocked
    :param inside_iter:
        int, how many swaps to make
    :param file_to_read:
        string, directory to read from
    :param file_to_save:
        string, directory to save to
    :return:
        Saves matrix calculated by TS algorithm
    """
    m = np.genfromtxt(file_to_read, delimiter=',')
    if headers:
        m = m[1:][:]
    if init_swap:
        solution = initrandomswap_m(m)
    else:
        solution = m
    print(calculate_time_matrices(m))
    tabu_list = np.zeros((len(m), len(m)))
    times = []
    for i in range(1, inside_iter):
        start = time.time()
        print(i)
        tm = calculate_time_matrices(solution)
        times.append(tm)
        print(tm)
        move = calculate_moves2(solution, tabu_list, allow_zeros)
        print(move)
        solution = swap(solution, move[0], move[1])
        tabu_list = update_tabu_list(tabu_list)
        tabu_list[move[0], move[1]] = s
        print("time per inside iter :", time.time() - start)
    np.savetxt(file_to_save, solution, delimiter=",")
    print("FINAL FOR ", s, "BLOCKS ", inside_iter, "INSIDE ITERATIONS ", "SAVED TO ", file_to_save)
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
ts(s=12,
   inside_iter=100,
   file_to_read="dane3.csv",
   file_to_save='dane3TS.csv',
   allow_zeros=True,
   headers=True,
   init_swap=True)
