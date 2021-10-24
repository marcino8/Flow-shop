import numpy as np
import pandas as pd


class Move:
    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.time = time  # new time - old time // if lower then zero we're happy // the lower the better


def initrandomswap(df):
    for i in range(1, 300):
        df, x, y = randomswap(df)
    return df


def calculate_moves(df, n):
    moves = []
    for i in range(1, n-1):
        for j in range(i + 1, n):
            df2 = swap(df, i, j)
            moves.append(Move(i, j, calculate_time(df2) - calculate_time(df)))  # new time - old time
    return moves


def swap(df, x, y):
    temp = df.iloc[x]
    df.loc[x] = df.iloc[y]
    df.loc[y] = temp
    df = df.reset_index(drop=True)
    return df


def randomswap(df):
    where_to_put, what_to_put = generate_swap_indexes(df)
    temp = df.iloc[where_to_put]
    df.loc[where_to_put] = df.iloc[what_to_put]
    df.loc[what_to_put] = temp
    df = df.reset_index(drop=True)
    return df, where_to_put, what_to_put


def generate_swap_indexes(df):
    return [np.random.randint(1, len(df.index)), np.random.randint(1, len(df.index))]


def is_not_present_in_tl(move, tl):
    return 0 == tl[move.x][move.y]


def select_best_move(moves, tl):
    best = Move(-1, -1, 99999)
    for move in moves:
        if is_not_present_in_tl(move, tl):
            if best.time > move.time:
                best = move
    return best


def update_tabu_list(tl):
    for move in tl:
        for value in move:
            if value > 0:
                value = value - 1
    return tl


def ts(df, s):
    tabu_list = np.zeros((len(df.index), len(df.index)))
    solution = initrandomswap(df)
    for i in range(1, 1000):
        moves = calculate_moves(solution, len(df.index))
        best_move = select_best_move(moves, tabu_list)
        solution = swap(solution, best_move.x, best_move.y)
        tabu_list = update_tabu_list(tabu_list)
        tabu_list[best_move.x][best_move.y] = s
        print(i)
    return solution


def calculate_time(df):
    df_calc = df.iloc[:, 1:]
    df_calc = df_calc.reset_index()
    df_calc = df_calc.iloc[:, 1:]
    itr = 0
    for col in df_calc.columns:
        for row in df_calc.index:
            current = df_calc.at[row, col]
            if row == 0 and itr == 0:
                df_calc.at[row, col] = current
            elif row == 0:
                df_calc.at[row, col] = current
            elif itr == 0:
                previous_job = df_calc.at[row - 1, col]
                df_calc.at[row, col] = previous_job + current
            else:
                previous_job = df_calc.at[row - 1, col]
                previous_task = df_calc.at[row, df_calc.columns[itr - 1]]
                df_calc.at[row, col] = max(previous_job, previous_task) + current
        itr = itr + 1
    return df_calc.iloc[len(df_calc.index) - 1, len(df_calc.columns) - 2]


def load(isOrdered):
    df = pd.read_csv("dane1.csv")
    if isOrdered:
        df = df.iloc[:, 1:]
    print(df.index)
    final = ts(df, 3)
    print(calculate_time(final))


load(True)
