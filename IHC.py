import numpy as np
import pandas as pd
import copy
import time


# def initrandomswap(df):
#     df2=copy.copy(df)
#     for i in range(1, 300):
#         randomswap(df2)
#     return df2


def initrandomswap_m(m):
    m2=copy.copy(m)
    for i in range(1,300):
        randomswap_m(m2)
    return m2


# def randomswap(df):
#     df2=copy.copy(df)
#     where_to_put, what_to_put = generate_swap_indexes(df2)
#     temp = df2.iloc[where_to_put]
#     df2.loc[where_to_put] = df2.iloc[what_to_put]
#     df2.loc[what_to_put] = temp
#     df2 = df2.reset_index(drop=True)
#     return df2

def randomswap_m(m):
    where_to_put, what_to_put = generate_swap_indexes_m(m)
    temp = m[where_to_put]
    m[where_to_put] = m[what_to_put]
    m[what_to_put] = temp
    return m

# def generate_swap_indexes(df):
#     return [np.random.randint(1, len(df.index)), np.random.randint(1, len(df.index))]

def generate_swap_indexes_m(m):
    return [np.random.randint(1, len(m)), np.random.randint(1, len(m))]

def ihc(m):
    tasks = len(m[0])
    best_solution = initrandomswap_m(m)
    for j in range(1,100):
        print(j)
        solution = initrandomswap_m(m)
        for i in range(1, (tasks-1)**2):
            m2 = randomswap_m(solution)
            t1 = calculate_time_matrices(solution)
            t2 = calculate_time_matrices(m2)
            delta_time = t2 - t1
            if delta_time < 0:
                solution = m2
        if calculate_time_matrices(best_solution)-calculate_time_matrices(solution) > 0:
            best_solution = solution
        print(calculate_time_matrices(best_solution))
    return best_solution


# def calculate_time(df):
#     df_calc = df.iloc[:, 1:]
#     df_calc = df_calc.reset_index()
#     df_calc = df_calc.iloc[:, 1:]
#     itr = 0
#     for col in df_calc.columns:
#         for row in df_calc.index:
#             current = df_calc.at[row, col]
#             if row == 0 and itr == 0:
#                 df_calc.at[row, col] = current
#             elif row == 0:
#                 df_calc.at[row, col] = current+df_calc.at[row, df_calc.columns[itr - 1]]
#             elif itr == 0:
#                 previous_job = df_calc.at[row - 1, col]
#                 df_calc.at[row, col] = previous_job + current
#             else:
#                 previous_job = df_calc.at[row - 1, col]
#                 previous_task = df_calc.at[row, df_calc.columns[itr - 1]]
#                 df_calc.at[row, col] = max(previous_job, previous_task) + current
#         itr = itr + 1
#     return df_calc.iloc[len(df_calc.index) - 1, len(df_calc.columns) - 2]


def calculate_time_matrices(matrix):
    m=copy.copy(matrix)
    for row in range(0, len(m)):
        for el in range(0, len(m[0])):
            if row == 0 and el == 0:
                pass
            elif row == 0:
                m[row][el] += m[row, el-1]
            elif el == 0:
                m[row][el] += m[row-1][el]
            else:
                m[row][el] += max(m[row-1][el], m[row][el-1])
    return m[len(m)-1][len(m[0])-1]

def load(isOrdered):
    df = pd.read_csv("dane2.csv")
    if isOrdered:
        df = df.iloc[:, 1:]
    print(df.index)
    final = ihc(df)
    final.to_csv("dane2_ihc.csv", sep=",")
    print(calculate_time_matrices(final))


matrix = np.random.randint(8,21,size=(200,20))
matrix=initrandomswap_m(matrix)
print(matrix)
print("works")
print(calculate_time_matrices(matrix))
ihc(matrix)