import copy
import numpy as np


def sum_row(m):
    """
    :param m:
        np matrix object
    :return:
        List of sums for every row in given martix
    """
    sums = []
    m=m[:,1:]
    for row in m:
        sums.append([sum(row)])
    return sums


def load(file_to_read, file_to_save):
    """
    :param file_to_read:
        file to read
    :param file_to_save:
        file to save
    :return:
        Saves matrix calculated by NEH algorythm
    """
    # load matrix
    matrix = np.genfromtxt(file_to_read, delimiter=',')
    # transform matrix
    matrix = matrix[1:][:]
    print(matrix)
    matrix = np.append(matrix, sum_row(matrix), axis=1)
    matrix = matrix[matrix[:, -1].argsort()]
    matrix = np.flip(matrix, axis=0)
    # set up 2 first rows
    first = matrix[0:2, :]
    second = np.flip(first, axis=0)
    # position 2 first rows
    if calculate_time_matrices(first) > calculate_time_matrices(second):
        start = second
    else:
        start = first
    # start neh
    for i in range(2, len(matrix)):
        start = neh(start, matrix[i])
        print(calculate_time_matrices(start))
    np.savetxt(file_to_save, start, delimiter=",")


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
    return m[len(m) - 1][len(m[0]) - 2]


def neh(m, new_row):
    """
    :param m:
        np matrix obj, matrix to insert new_row into every possible
        position and find the best using calculate_time_matrices()
    :param new_row:
        np array obj, row to be inserted
    :return:
        np matrix obj, with new_row inserted to m, at the best possible position
    """
    mintime = 99999999
    pos = 0
    for i in range(0, len(m) + 1):
        df2 = insert_row(m, new_row, i)
        czas = calculate_time_matrices(df2)
        if czas < mintime:
            mintime = czas
            pos = i
    df2 = insert_row(m, new_row, pos)
    return df2


def insert_row(m, row, row_index):
    """
    :param m:
        np matrix obj, matrix to insert the row
    :param row:
        np array obj, row to be inserted
    :param row_index:
        int, index where to insert the row in m
    :return:
        np matrix obj, matrix with inserted row to m at position row_index
    """
    m = np.insert(m, row_index, row, 0)
    return m


load("dane1.csv", "dane2_neh.csv")
