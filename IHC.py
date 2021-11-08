
import time
import numpy as np
from numpy import genfromtxt
import Calculations as Calc


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
        best_solution = Calc.initrandomswap_m(m)
    else:
        best_solution = m
    print(Calc.calculate_time_matrices(m))
    print(Calc.calculate_time_matrices(best_solution))
    times = []
    times2 = []
    for j in range(0, outside_iter):
        start = time.time()
        print("OUTSIDE ITER:", j)
        solution = Calc.initrandomswap_m(m)
        no_change = 0
        for i in range(0, indide_iter):
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
            else:
                no_change += 1
            if no_change > no_change_number:
                break
        tm = Calc.calculate_time_matrices(best_solution)
        tm2 = Calc.calculate_time_matrices(solution)
        if tm - tm2 > 0:
            best_solution = solution
        print(tm)
        times.append(tm)
        times2.append(tm2)
        print("time per outside iter :", time.time() - start)
    np.savetxt(file_to_save, best_solution, delimiter=",")
    print("FINAL FOR ", indide_iter, "INSIDE ITER ", outside_iter, "OUTSIDE ITER ", "WITH NO CHANGE ", no_change_number,
          "SAVED TO ", file_to_save)
    Calc.ploted(
        x=np.linspace(1, outside_iter, outside_iter),
        y1=times,
        y2=times2,
        xlab="TIME",
        ylab="ITER",
        y1lab="pretender times for " + str(indide_iter) + " new iter",
        y2lab="best times for overall iter",
        title="IHC",
        savename=file_to_save)


ihc(outside_iter=100,
    indide_iter=20000,
    no_change_number=99999,
    file_to_read="dane3.csv",
    file_to_save="dane3ihc.csv",
    init_swap=True,
    headers=True)
