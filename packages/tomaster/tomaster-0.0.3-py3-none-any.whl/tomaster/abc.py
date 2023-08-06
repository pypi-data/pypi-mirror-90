from sklearn import datasets

from tomato import *
from tomato import _find

X, y = datasets.make_circles(n_samples=1000, noise=0.02, random_state=1337)

# parent, persistence, _ = tomato(points=X, k=10, raw=True, bandwidth=.1)
##print(sorted(persistence)[-10:])

# import matplotlib.pyplot as plt
# c, neigh = tomato(points=X, k=10, raw=False, bandwidth=.1,keep_cluster_labels=True)

# plt.scatter(*X.T, c=c)

# for i in range(len(X)):
#    for j in neigh[i]:
#        plt.plot(*X[[i,j]].T, 'k-', linewidth='.1')
# plt.show()

# for i in range(len(X)):
#    for j in neigh[i]:
#        if int(X[i][1] < 0.2) + int(X[j][1] < 0.2)  == 1:
#            if c[i] == c[j] == 1:
#                print(i, j)

from numba import njit
from numba.typed import List


@njit
def f(n):
    return np.arange(n)


points = X
k = 20
distances, neighbors = NearestNeighbors(n_neighbors=k).fit(points).kneighbors()
bandwidth = 0.05
density = np.exp(-((distances / bandwidth) ** 2)).sum(axis=-1)

c = tomato(points=X, k=k, bandwidth=bandwidth, keep_cluster_labels=False)

r  = tomato(points=X, k=k, bandwidth=bandwidth, raw=True)
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

c = tomato(points=X, k=k, bandwidth=bandwidth, keep_cluster_labels=False, n_clusters=3)
edges  = tomato(points=X, k=k, bandwidth=bandwidth, raw=True)
sp = sorted((p for p, _, _ in edges), reverse=True)

plt.scatter(*X.T, c=c)
for _, i, j in r:
        plt.plot(*X[[i,j]].T, 'k-', linewidth='.1')

plt.show()


n = len(density)
forest = np.empty(n, dtype=np.int64)


ind = density.argsort()[::-1]
order = ind.argsort()

for i in ind:
    forest[i] = i
    for j in neighbors[i]:
        if order[j] < order[forest[i]]:
            forest[i] = j

    if forest[i] == i:
        continue
    ri = _find(forest, i)

    for j in neighbors[i]:
        if order[j] > order[i]:
            continue
        rj = _find(forest, j)
        if ri == rj:
            continue
        if order[ri] < order[rj]:
            if density[rj] - density[i]  < 0.002:

                forest[rj] = ri
        else:
            if density[ri] - density[i] < 0.002:
                forest[ri] = ri = rj

for i in range(n):
    _find(forest, i)
plt.scatter(*X.T, c=forest)
for _, i, j in r:
        plt.plot(*X[[i,j]].T, 'k-', linewidth='.1')

plt.show()

# plt.show()
# k = 5
# distances, neighbors = NearestNeighbors(n_neighbors=k).fit(X).kneighbors()
# density = ((distances ** 2).mean(axis=-1) + 1e-10) ** -0.5

# tau = 0.5
# forest, parent, persistence = _tomato(density, neighbors, tau)


# for i, j in enumerate(parent):
#    assert density[i] <= density[j]
#    assert persistence[i] <= persistence[j]

