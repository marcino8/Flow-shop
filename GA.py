import copy
from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt

def initrandomswap_m(m):
    """
        :param m:
            np matrix obj, to randomly swap its rows
        :return:
            np matrix obj, with randomly swapped rows 5000 times
    """
    m2 = copy.copy(m)
    for i in range(1, 500):
        randomswap_m(m2)
    return m2


def randomswap_m(m):
    """
        :param m:
            np matrix obj, matrix to swap 2 random rows
        :return:
            np matrix obj, m2 with swapped two random rows
    """
    where_to_put, what_to_put = generate_swap_indexes_m(m)
    m[[where_to_put, what_to_put]] = m[[what_to_put, where_to_put]]
    return m


def generate_swap_indexes_m(m):
    """
        :param m:
            obj to get ist lengths
        :return:
            List of 2 ints, being 2 random integer numbers from 0 to length of m exclusive
    """
    return [np.random.randint(1, len(m)), np.random.randint(1, len(m))]


def initrandomswaps_m(m, n):
    """
    Initiates population size n using initrandomswap on m
    """
    population = []
    for i in range(0, n):
        population.append(initrandomswap_m(m))
    return population


def select_best_solutions(population, n):
    """
    Select pairs to cross from population
    The parents are beeing chosen according to dist. function intervals.
    :param population:
        list of np matrix obj, list from which to chose matrices to cross
    :param n:
        int, size of population
    :return:
        n/2 element list of 2 np matrixes,
        meaning returns n/2 pairs ready to be crossed
    """
    population_with_times = []
    suma = 0
    # calculate times for everyone in population
    ind = 0
    for parent in population:
        s = calculate_time_matrices(parent)
        population_with_times.append([ind, s])
        suma += s
        ind += 1
    # divide time by sum of all times to get the probablilities
    for parent_and_time in population_with_times:
        parent_and_time[1] = parent_and_time[1] / suma
    # sort population and times by probablilities
    sorted(population_with_times, key=lambda x: x[1])
    poprzedni = 0
    # change probabilities to distribution
    for parent_and_time in population_with_times:
        temp = parent_and_time[1]
        parent_and_time[1] = poprzedni + parent_and_time[1]
        poprzedni += temp
    # reverse distribution (the lower the higher change to pick)
    d = []
    for parent_and_time in population_with_times:
        d.append(parent_and_time[1])
    d.reverse()
    # replace distribution with the reversed one
    reversed_parent_and_time = []
    for i in range(0, len(d)):
        reversed_parent_and_time.append([population_with_times[i][0], d[i]])
    reversed_parent_and_time.reverse()
    # select pairs from population according to population size and distribution intervals
    selected_population = []
    for i in range(1, int(n / 2) + 1):
        parents = []
        while len(parents) != 2:
            random = np.random.random()
            for parent_and_time in reversed_parent_and_time:
                if parent_and_time[1] < random and parent_and_time[0] not in parents:
                    parents.append(parent_and_time[0])
                    break
            selected_population.append(parents)
    all_pairs = []
    for p in selected_population:
        all_pairs.append([population[p[0]], population[p[1]]])
    return all_pairs


def mutate_children(solutions, rswaps):
    """
    Mutate every matrix in population, meaning make rswaps number of random
    swaps in every matrix in solutions
    """
    for solution in solutions:
        for i in range(0, rswaps):
            solution = randomswap_m(solution)
    return solutions


def select_best_child(solutions):
    """
    Select best matrix from current population
    """
    min = calculate_time_matrices(solutions[0])
    mat = solutions[0]
    for solution in solutions:
        if calculate_time_matrices(solution) < min:
            mat = solution
    return mat


def not_present_in_solution(m, target):
    indexes = m[0, :]
    for i in indexes:
        if i == target:
            return False


def cross_indexes(tasks1, tasks2, div1, div2):
    tasks = []
    start = div1
    end = div2
    for i in range(start, end):
        tasks.append(tasks1[i])
    for i in range(end, len(tasks1)):
        if tasks2[i] not in tasks:
            tasks.append(tasks2[i])
    for i in range(0, len(tasks1)):
        if tasks2[i] not in tasks:
            tasks.append(tasks2[i])
    tasks3 = []
    for i in range(start, end):
        tasks3.append(tasks2[i])
    for i in range(end, len(tasks1)):
        if tasks1[i] not in tasks3:
            tasks3.append(tasks1[i])
    for i in range(0, len(tasks1)):
        if tasks1[i] not in tasks3:
            tasks3.append(tasks1[i])
    return tasks3, tasks


def build_from_indexes(m, idx):
    for row in m:
        if row[0] == idx[0]:
            mat = row
    for i in idx[1:]:
        for row in m:
            if row[0] == i:
                mat = np.vstack((mat, row))
    return mat


def produce_children1(parents, div1, div2):
    new_population = []
    for pair in parents:
        ch_indx1, ch_indx2 = cross_indexes(pair[0][:, 0], pair[1][:, 0], div1, div2)
        child1 = build_from_indexes(pair[0], ch_indx1)
        child2 = build_from_indexes(pair[0], ch_indx2)
        new_population.append(child1)
        new_population.append(child2)
    return new_population


def ploted(x, y1, y2, ylab, xlab, y1lab, y2lab, title, savename):
    plt.plot(x, y1, label=y1lab)
    plt.plot(x, y2, label=y2lab)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.title(title)
    plt.legend()
    plt.savefig(savename+"wykres.jpeg")


def ga(population_size, iterations, mutations,  div1, div2, file_to_read, file_to_save):
    m = genfromtxt(file_to_read, delimiter=',')
    m = m[1:][:]
    population = initrandomswaps_m(m, population_size)
    best = select_best_child(population)
    print(best, calculate_time_matrices(best))
    epoch = 1
    epochs = np.linspace(1, population_size, population_size)
    times1 = []
    times2 = []
    while epoch <= iterations:
        parents = select_best_solutions(population, population_size)
        children = produce_children1(parents, div1, div2)
        population = mutate_children(children, mutations)
        pretender = select_best_child(population)
        pr_time = calculate_time_matrices(pretender)
        best_time = calculate_time_matrices(best)
        if pr_time < best_time:
            best = pretender
        print(best_time, epoch)
        times1.append(pr_time)
        times2.append(best_time)
        epoch+=1
    np.savetxt(file_to_save, best, delimiter=",")
    ploted(
           x=epochs,
           y1=times1,
           y2=times2,
           xlab="TIME",
           ylab="EPOCH",
           y1lab="pretender times for "+str(population_size)+"popualtion",
           y2lab="best unit times for "+str(population_size)+"popualtion",
           title="GA",
           savename=file_to_save)


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


ga(100, 100, 4, 50, 100, "dane2.csv", "dane2_ga_100_100_4_50_100.csv")
