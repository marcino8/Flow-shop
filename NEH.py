import numpy as np
import Calculations as Calc


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
    matrix = np.append(matrix, Calc.sum_row(matrix), axis=1)
    matrix = matrix[matrix[:, -1].argsort()]
    matrix = np.flip(matrix, axis=0)
    # set up 2 first rows
    first = matrix[0:2, :]
    second = np.flip(first, axis=0)
    # position 2 first rows
    if Calc.calculate_time_matrices_neh(first) > Calc.calculate_time_matrices_neh(second):
        start = second
    else:
        start = first
    # start neh
    for i in range(2, len(matrix)):
        start = neh(start, matrix[i])
        print(Calc.calculate_time_matrices_neh(start))
    np.savetxt(file_to_save, start, delimiter=",")


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
        df2 = Calc.insert_row(m, new_row, i)
        czas = Calc.calculate_time_matrices_neh(df2)
        if czas < mintime:
            mintime = czas
            pos = i
    df2 = Calc.insert_row(m, new_row, pos)
    return df2


load("dane1.csv", "dane2_neh.csv")
