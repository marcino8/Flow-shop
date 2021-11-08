import copy

from numpy import genfromtxt

m = genfromtxt("dane3xd2.csv", delimiter=',')
m = copy.copy(m[:, 1:])
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
print(m[len(m) - 1][len(m[0]) - 1])
