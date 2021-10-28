import itertools
import time
from numba import jit, cuda

import numpy as np
import pandas as pd
import copy


class Move:
    def __init__(self, x, y, time): #
        self.x = x
        self.y = y
        self.time = time  # new time - old time // if lower then zero we're happy // the lower the better


def initrandomswap_m(m):
    m2 = copy.copy(m)
    for i in range(1, 300):
        randomswap_m(m2)
    return m2


def is_better_then_in_list(list, dt, x, y, s):
    if len(list) > s*5:
        maks = Move(-1, -1, -892176394572)
        dum = False
        for el in list:
            if dt < el.time:
                dum = True
            if el.time > maks.time:
                maks = el
        if dum:
            list.append(Move(x, y, dt))
            list.remove(maks)
    else:
        list.append(Move(x, y, dt))
    return list


def calculate_moves(m, s):
    moves = []
    for i in range(1, len(m)):
        for j in range(i + 1, len(m)):
            m2 = swap(m, i, j)
            delta_time = calculate_time_matrices(m2) - calculate_time_matrices(m)
            moves = is_better_then_in_list(moves, delta_time, i, j, s)

    return moves


def swap(mt, x, y):
    m=copy.copy(mt)
    temp = m[x]
    m[x] = m[y]
    m[y] = temp
    return m


def randomswap_m(m):
    where_to_put, what_to_put = generate_swap_indexes_m(m)
    temp = m[where_to_put]
    m[where_to_put] = m[what_to_put]
    m[what_to_put] = temp
    return m


def generate_swap_indexes_m(m):
    return [np.random.randint(1, len(m)), np.random.randint(1, len(m))]


def is_not_present_in_tl(move, tl):
    return 0 == tl[move.x][move.y] and 0 == tl[move.y][move.x]


def select_best_move(moves, tl):
    best=moves[0]
    for move in moves:
        if is_not_present_in_tl(move, tl):
            if best.time > move.time:
                best = move
    return best


def update_tabu_list(tl):
    for i in range(0, len(m)):
        for j in range(0,len(m[0])):
            if tl[i][j] > 0:
                tl[i][j] -= 1
    return tl


def ts(m, s):
    tabu_list = np.zeros((len(m), len(m)))
    solution = initrandomswap_m(m)
    for i in range(1, 1000):
        print(i)
        print(calculate_time_matrices(solution))
        moves = calculate_moves(solution, s)
        best_move = select_best_move(moves, tabu_list)
        print(best_move.x,best_move.y,best_move.time)
        solution = swap(solution, best_move.x, best_move.y)
        tabu_list = update_tabu_list(tabu_list)
        tabu_list[best_move.x][best_move.y] = s
        np.savetxt("dane2_ts_10.csv", solution, delimiter=",")
    return solution


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



def load(s):
    df = np.genfromtxt('dane2.csv', delimiter=',')
    df = df[1:][:]
    final = ts(df, s)
    np.savetxt("dane2_ts_10.csv", final, delimiter=",")
    print(calculate_time_matrices(final))



load(10)
