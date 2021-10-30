import copy
from numpy import genfromtxt
import numpy as np


def initrandomswap_m(m):
    m2 = copy.copy(m)
    for i in range(1, 5000):
        randomswap_m(m2)
    return m2



def randomswap_m(mt):
    m=copy.copy(mt)
    where_to_put, what_to_put = generate_swap_indexes_m(m)
    temp = m[where_to_put]
    m[where_to_put] = m[what_to_put]
    m[what_to_put] = temp
    return m



def generate_swap_indexes_m(m):
    return [np.random.randint(1, len(m)), np.random.randint(1, len(m))]


def initrandomswaps_m(n, m):
    population = []
    for i in range(1,n):
        population.append(randomswap_m(m))
    return population


def lower_than_max(new, top_solutions):
    max_el = top_solutions[0]
    for solution in top_solutions:
        if solution[1] > max_el[1]:
            max_el=solution
    if new[1]<max_el[1]:
        top_solutions.remove(max_el)
        top_solutions.append(new)



def select_best_solutions(population, n):
    top_solutions = []
    for solution in population:
        if len(top_solutions) < n/2:
            top_solutions.append([solution, calculate_time_matrices(solution)])
        else:
            new = []
            new.append(solution)
            new.append(calculate_time_matrices(solution))
            lower_than_max(new, top_solutions)
    return top_solutions


def mutate_children(solutions, rswaps):
    for solution in solutions:
        for i in range(1,rswaps):
            solution = randomswap_m(solution)
    return solutions


def select_best_child(solutions):
    min = solutions[0]
    for solution in solutions:
        if solution[1] < min[1]:
            min = solution
    return min


def produce_children():
    pass


def ga(m,n):
    population = initrandomswaps_m(m, n)
    epoch=1
    while epoch<1000000:
        select_best_solutions(population,n)
        produce_children()
        population = mutate_children()
        select_best_child()
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


def load():
    df = genfromtxt('dane2.csv', delimiter=',')
    df = df[1:][:]
    final = sa(df)
    np.savetxt("dane2_sa099_092.csv", final, delimiter=",")
    print(calculate_time_matrices(final))


load()