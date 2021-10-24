import copy

import numpy as np
import pandas as pd


def initrandomswap(df):
    for i in range(1, 300):
        randomswap(df)
    return df


def randomswap(df):
    df2=copy.copy(df)
    where_to_put, what_to_put = generate_swap_indexes(df2)
    temp = df2.iloc[where_to_put]
    df2.loc[where_to_put] = df2.iloc[what_to_put]
    df2.loc[what_to_put] = temp
    df2 = df2.reset_index(drop=True)
    return df2


def generate_swap_indexes(df):
    return [np.random.randint(1, len(df.index)), np.random.randint(1, len(df.index))]


def sa(df):
    t = 0.9
    tasks = len(df.index)
    solution = initrandomswap(df)
    while t > 0.0000001:
        print(t)
        for i in range(1, (tasks - 1) ^ 2):
            df2 = randomswap(solution)
            t1 = calculate_time(solution)
            t2 = calculate_time(df2)
            delta_time = t2 - t1
            if delta_time < 0:
                solution = df2
            elif np.random.random() > np.exp((-1) * delta_time / t):
                solution = df2
        t = t * 0.75
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
    df = pd.read_csv("dane2.csv")
    if isOrdered:
        df = df.iloc[:, 1:]
    print(df.index)
    final = sa(df)
    final.to_csv("dane2_sa.csv", sep=",")
    print(calculate_time(final))


load(True)
