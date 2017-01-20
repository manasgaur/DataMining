from cvxopt import matrix, solvers, spmatrix
import numpy as np
import matplotlib.pyplot as plt
from math import *

def main():
    data = [[6.0,7,-1], [7,7,-1], [3,5,1], [4,5,1]]
    Q = spmatrix(2.0, range(3), range(3))
    Q[2,2] = 0
    p = matrix([0.0, 0.0, 0.0], (3,1))
    G = []
    h = []
    for items in data:
        row = []
        if items[2] == 1:
            row.extend([-1 * item for item in items[:2]])
            row.append(-1)
            G.append(row)
            h.append(-1.0)
        else:
            row.extend(items[:2])
            row.append(1)
            G.append(row)
            h.append(-1.0)
    G = matrix(G).trans()
    h = matrix(h)
    A = None
    b = None
    sol=solvers.qp(Q, p, G, h)
    w1 = sol['x'][0]
    w2 = sol['x'][1]
    b  = sol['x'][2]
    print 'w1= {0}; w2={1}; b={2}'.format(w1, w2, b)

    ### suppose you have obtained sol['x'] from CVXOPT QP minimization

    x = [item[0] for item in data if item[2] == 1]
    y = [item[1] for item in data if item[2] == 1]
    plt.scatter(x, y, s=80, facecolors='none', edgecolors='r')
    x = [item[0] for item in data if item[2] == -1]
    y = [item[1] for item in data if item[2] == -1]
    plt.scatter(x, y, s=80, facecolors='none', edgecolors='b')
    x = [item[0] for item in data]
    y = [item[1] for item in data]
    plt.scatter(x, y, s=40, facecolors='none', edgecolors='k')
    w1 = sol['x'][0]
    w2 = sol['x'][1]
    b = sol['x'][2]

    print 'Answer to question a:'
    print 'w: {0}; b: {1} \n'.format([w1,w2], b)
    print 'Answer to question b:'
    for point in data:
        print '{0}: {1}'.format(point, abs(w1 * point[0] + w2 * point[1] + b)/sqrt(w1 * w1 + w2 * w2))

    print '\nAnswer to question c: '
    print 2/sqrt(w1 * w1 + w2 * w2)

    print '\nAnswer to question d:'
    print 'w.x + b > 0 for positive class'
    print 'w.x + b < 0 for negative class'

    new_points = [[5, 3], [3, 5], [6, 6], [5, 6], [6, 5]]

    print '\nAnswer to question c:'
    for point in new_points:
        if w1 * point[0] + w2 * point[1] + b < 0:
            print '{0}: {1}'.format(point, 'FALSE')
        else:
            print '{0}: {1}'.format(point, 'TRUE')

    x = [min([item[0] for item in data]), max([item[0] for item in data])]

    y = [(w1 * x[i] + b)/(-1 * w2) for i in range(2)]

    plt.plot(x, y, color='red')

    y = [(w1 * x[i] + b - 1)/(-1 * w2) for i in range(2)]

    plt.plot(x, y, color='black')

    y = [(w1 * x[i] + b + 1)/(-1 * w2) for i in range(2)]

    plt.plot(x, y, color='black')

    plt.gca().set_aspect('equal', adjustable='box')

    plt.grid()

    plt.show()


if __name__ == '__main__':
    main()