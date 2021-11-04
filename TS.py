import time
import numpy as np
import copy
import matplotlib.pyplot as plt


def initrandomswap_m(m):
    m2 = copy.copy(m)
    for i in range(1, 300):
        randomswap_m(m2)
    return m2


def calculate_moves2(m, tl):
    move = [0, 0, 99999]
    for i in range(1, len(m)):
        for j in range(i + 1, len(m)):
            if is_not_present_in_tl(tl, i, j):
                m2 = swap(m, i, j)
                delta_time = calculate_time_matrices(m2) - calculate_time_matrices(m)
                if delta_time < move[2]:
                    move = [i, j, delta_time]
    return move


def swap(mt, x, y):
    m = copy.copy(mt)
    m[[x,y]] = m[[y,x]]
    return m


def randomswap_m(mt):
    m = copy.copy(mt)
    where_to_put, what_to_put = generate_swap_indexes_m(m)
    m[[where_to_put,what_to_put]] = m[[what_to_put,where_to_put]]
    return m


def generate_swap_indexes_m(m):
    return [np.random.randint(0, len(m)), np.random.randint(0, len(m))]


def is_not_present_in_tl(tl, i, j):
    return 0 == tl[i, j] and 0 == tl[j, i]


def update_tabu_list(tl):
    for i in range(0, len(tl)):
        for j in range(0, len(tl)):
            if tl[i][j] > 0:
                tl[i][j] -= 1
    return tl


def ts(s, inside_iter, file_to_read, file_to_save):
    m = np.genfromtxt(file_to_read, delimiter=',')
    m = m[1:][:]
    tabu_list = np.zeros((len(m), len(m)))
    solution = initrandomswap_m(m)
    times = []
    for i in range(1, inside_iter):
        start = time.time()
        print(i)
        tm = calculate_time_matrices(solution)
        times.append(tm)
        print(tm)
        move = calculate_moves2(solution, tabu_list)
        print(move)
        solution = swap(solution, move[0], move[1])
        tabu_list = update_tabu_list(tabu_list)
        tabu_list[move[0], move[1]] = s
        print("time per inside iter :",time.time() - start)
    np.savetxt(file_to_save, solution, delimiter=",")
    print("FINAL FOR ", s, "BLOCKS ", inside_iter, "INSIDE ITERATIONS ", "SAVED TO ", file_to_save)
    plt.plot(times)
    plt.ylabel("czas")
    plt.show()
    save = file_to_save+".jpeg"
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





# ts(5,1000, 'dane2.csv','dane2_ts_2_500.csv')
ts(5,100, 'dane2.csv','dane2_ts_5_100.csv')
ts(10,100, 'dane2.csv','dane2_ts_10_100.csv')
ts(20,100, 'dane2.csv','dane2_ts_20_100.csv')
ts(5,500, 'dane2.csv','dane2_ts_5_500.csv')
ts(5,200, 'dane2.csv','dane2_ts_5_200.csv')



