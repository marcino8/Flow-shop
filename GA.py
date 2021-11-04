import copy
from numpy import genfromtxt
import numpy as np


def initrandomswap_m(m):
    m2 = copy.copy(m)
    for i in range(1, 5000):
        randomswap_m(m2)
    return m2


def randomswap_m(m):
    where_to_put, what_to_put = generate_swap_indexes_m(m)
    m[[where_to_put, what_to_put]] = m[[what_to_put, where_to_put]]
    return m


def generate_swap_indexes_m(m):
    return [np.random.randint(1, len(m)), np.random.randint(1, len(m))]


def initrandomswaps_m(m, n):
    population = []
    for i in range(1, n):
        population.append(initrandomswap_m(m))
    return population


def lower_than_max(new, top_solutions):
    max_el = top_solutions[0]
    for solution in top_solutions:
        if solution[1] > max_el[1]:
            max_el = solution
    if new[1] < max_el[1]:
        top_solutions.remove(max_el)
        top_solutions.append(new)


def select_best_solutions(population, n):
    population_with_times = []
    suma = 0
    for parent in population:
        s = calculate_time_matrices(parent)
        population_with_times.append([parent, s])
        suma += s
    for parent_and_time in population_with_times:
        parent_and_time[1] = parent_and_time[1] / suma
    sorted(population_with_times, key=lambda x: x[1])
    poprzedni = 0
    for parent_and_time in population_with_times:
        temp = parent_and_time[1]
        parent_and_time[1] = poprzedni + parent_and_time[1]
        poprzedni += temp
    d =[]
    for parent_and_time in population_with_times:
        d.append(parent_and_time[1])
    d.reverse()
    reversed_parent_and_time = []
    for i in range(0, len(d)):
        reversed_parent_and_time.append([population_with_times[i][0], d[i]])
    reversed_parent_and_time.reverse()

    selected_population = []
    for i in range(1, int(n/2)):
        parents=[]
        for j in range(0,2):
            for parent_and_time in reversed_parent_and_time:
                if parent_and_time[1] < np.random.random():
                    parents.append(parent_and_time[0])
                    break
        selected_population.append(parents)
        print("APPENDED PARENTS WITH")
        print(parents)
    return selected_population


def mutate_children(solutions, rswaps):
    for solution in solutions:
        for i in range(1, rswaps):
            solution = randomswap_m(solution)
    return solutions


def select_best_child(solutions):
    min = solutions[0]
    for solution in solutions:
        if solution[1] < min[1]:
            min = solution
    return min


def not_present_in_solution(m, target):
    indexes = m[0,:]
    for i in indexes:
        if i==target:
            return False


def produce_children1(parents):
    first = int(len(parents[0][0])/3)
    last = int(2*len(parents[0][0])/3)
    for pair in parents:
        child1 = pair[0][first:last,:]
        for i in range(last, len(parents[0][0])):
            if not_present_in_solution(child1,pair[1][i,0]):
                np.vstack((child1, pair[1][i]))
        for i in range(0, last):
            if not_present_in_solution(child1,pair[1][i,0]):
                np.vstack((pair[1][i], child1))
        child2 = pair[1][first:last, :]
        for i in range(last, len(parents[0][0])):
            if not_present_in_solution(child2, pair[0][i,0]):
                np.vstack((child2, pair[0][i]))
        for i in range(0, last):
            if not_present_in_solution(child2, pair[0][i,0]):
                np.vstack((pair[0][i], child2))




def ga(m, n):
    population = initrandomswaps_m(m, n)
    epoch = 1
    while epoch < 1000:
        parents=select_best_solutions(population, n)
        print("PARENTS")
        print(parents)
        produce_children1()
        population = mutate_children()
        select_best_child()
    return 0


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


matrix = np.random.randint(1, 78, (5, 5))
ga(matrix, 6)
