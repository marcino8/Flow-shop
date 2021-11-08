import copy
from numpy import genfromtxt
import numpy as np
import Calculations as Calc


def ga(population_size, iterations, mutations, div1, div2, file_to_read, file_to_save):
    m = genfromtxt(file_to_read, delimiter=',')
    m = m[1:][:]
    population = Calc.initrandomswaps_m(m, population_size)
    best = Calc.select_best_child(population)
    print(best, Calc.calculate_time_matrices(best))
    epoch = 1
    times1 = []
    times2 = []
    while epoch <= iterations:
        parents = Calc.select_best_solutions(population, population_size)
        children = Calc.produce_children1(parents, div1, div2)
        population = Calc.mutate_children(children, mutations)
        pretender = Calc.select_best_child(population)
        pr_time = Calc.calculate_time_matrices(pretender)
        best_time = Calc.calculate_time_matrices(best)
        if pr_time < best_time:
            best = pretender
        print(best_time, epoch)
        times1.append(pr_time)
        times2.append(best_time)
        epoch += 1
    np.savetxt(file_to_save, best, delimiter=",")
    Calc.ploted(
        x=np.linspace(1, iterations, iterations),
        y1=times1,
        y2=times2,
        xlab="TIME",
        ylab="EPOCH",
        y1lab="pretender times for " + str(population_size) + " popualtion",
        y2lab="best unit times for " + str(population_size) + " popualtion",
        title="GA",
        savename=file_to_save)


ga(50, 1000, 2, 66, 132, "dane2.csv", "dane2_ga_200_1000_2_17_34.csv")
