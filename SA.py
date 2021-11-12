import time
from numpy import genfromtxt
import numpy as np
import Calculations as Calc


def sa(start_T, red_T, geom, inside_iter, no_change_number, file_to_read, file_to_save,
       headers=False, init_swap=False):
    """
    :param init_swap:
        bool, if true, swaps loaded from file solution
    :param headers:
        bool, if true, deletes headers
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
    if headers:
        m = m[1:][:]
    print(Calc.calculate_time_matrices(m))
    t = start_T
    if init_swap:
        solution = Calc.initrandomswap_m(m)
    else:
        solution = m
    times = []
    if geom:
        stop = 0.01
    else:
        stop = 0.00001
    while t > stop:
        start = time.time()
        tm = Calc.calculate_time_matrices(solution)
        print("TEMPERATURE", t, tm)
        no_change = 0
        times.append(tm)
        for i in range(1, inside_iter):
            rnd = np.random.randint(1, 4)
            if rnd == 1:
                m2 = Calc.randomswap_m(solution)
            elif rnd == 2:
                m2 = Calc.randomswap_m2(solution)
            else:
                m2 = Calc.randomswap_m3(solution)
            t1 = Calc.calculate_time_matrices(solution)
            t2 = Calc.calculate_time_matrices(m2)
            delta_time = t2 - t1
            if delta_time < 0:
                solution = m2
                no_change = 0
            elif np.random.random() < np.exp((-1) * delta_time / t):
                solution = m2
                no_change = 0
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
    return times

