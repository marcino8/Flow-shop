from numpy import genfromtxt
import numpy as np
import Calculations as Calc


def ga(population_size, iterations, mutations, div1, div2, cross, file_to_read, file_to_save):
    m = genfromtxt(file_to_read, delimiter=',')
    m = m[1:][:]
    population = Calc.initrandomswaps_m(m, population_size)
    best = Calc.select_best_child(population)
    print(best, Calc.calculate_time_matrices(best))
    epoch = 1
    times1 = []
    times2 = []
    times3 = []
    while epoch <= iterations:
        parents = Calc.select_best_solutions(population, population_size)
        children = Calc.produce_children1(parents, div1, div2, cross)
        population = Calc.mutate_children(children, mutations)
        pretender = Calc.select_best_child(population)
        pr_time = Calc.calculate_time_matrices(pretender)
        best_time = Calc.calculate_time_matrices(best)
        if pr_time < best_time:
            best = pretender
        print(best_time, epoch)
        times1.append(pr_time)
        times2.append(best_time)
        avg = 0
        for s in population:
            avg += Calc.calculate_time_matrices(s)
        avg /= len(population)
        times3.append(avg)
        epoch += 1
    np.savetxt(file_to_save, best, delimiter=",")
    Calc.plotedGA(
        x=np.linspace(1, iterations, iterations),
        y1=times1,
        y2=times2,
        y3=times3,
        xlab="TIME",
        ylab="EPOCH",
        y1lab="pretender times",
        y2lab="best unit times",
        y3lab="average time in population",
        title="GA psize " + str(population_size) + " epoch " + str(iterations) + " mutations " + str(mutations),
        savename=file_to_save)
