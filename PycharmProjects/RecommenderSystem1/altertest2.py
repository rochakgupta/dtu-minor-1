__author__ = 'rochak'

import collaborative
# Standard python modules
import sys

# For scientific computing
import numpy
from numpy import *
import scipy.io, scipy.misc, scipy.optimize, scipy.cluster.vq

# For plotting
import matplotlib
from matplotlib import pyplot, cm, colors, lines
from mpl_toolkits.mplot3d import Axes3D

from util import Util
from timeit import Timer
from sklearn.decomposition import RandomizedPCA


def pca(X):
    covariance = X.T.dot(X) / shape(X)[0]
    U, S, V = linalg.svd(covariance)
    return U, S


def projectData(X, U, K):
    return X.dot(U)[:, :K]


def kMeansInitCentroids(X, K):
    return random.permutation(X)[:K]


def findClosestCentroids(X, centroids):
    K = shape(centroids)[0]
    m = shape(X)[0]
    idx = zeros((m, 1))

    for i in range(0, m):
        cost = X[i] - centroids[0]
        lowest = cost.T.dot(cost)
        lowest_index = 0

        for k in range(1, K):
            cost = X[i] - centroids[k]
            cost = cost.T.dot(cost)
            if cost < lowest:
                lowest_index = k
                lowest = cost

        idx[i] = lowest_index

    return idx + 1  # add 1, since python's index starts at 0


def computeCentroids(X, idx, K):
    m, n = shape(X)
    centroids = zeros((K, n))

    data = c_[X, idx]  # append the cluster index to the X

    for k in range(1, K + 1):
        temp = data[data[:, n] == k]  # quickly extract X that falls into the cluster
        count = shape(temp)[0]  # count number of entries for that cluster

        for j in range(0, n):
            centroids[k - 1, j] = sum(temp[:, j]) / count

    return centroids


# b: blue
# g: green
# r: red
# c: cyan
# m: magenta
# y: yellow
# k: black
# w: white


def runkMeans(X, initial_centroids, max_iters, plot=False):
    K = shape(initial_centroids)[0]
    centroids = copy(initial_centroids)
    idx = None
    n = shape(X)[1]
    dict = {}
    c = 0
    for name, hex in matplotlib.colors.cnames.iteritems():
        dict[c] = name
        c += 1

    random.shuffle(dict)

    for iteration in range(0, max_iters):
        idx = findClosestCentroids(X, centroids)
        centroids = computeCentroids(X, idx, K)
        fig = pyplot.figure()
        if plot is True:
            data = c_[X, idx]
            for i in range(1, K + 1):
                data_1 = data[data[:, n] == i]
                pyplot.plot(data_1[:, 0], data_1[:, 1], linestyle=' ', color=dict[i - 1], marker='o', markersize=3)

            pyplot.plot(centroids[:, 0], centroids[:, 1], 'k*', markersize=15)
            fig.savefig('kMeans_{}.png'.format(iteration), dpi=300)
            pyplot.show(block=True)

    return centroids, idx


def kMeansClustering():

    prev_X = collaborative.collaborativeFiltering()
    X = prev_X
    X_norm, mu, sigma = Util.featureNormalize(X)
    U, S = pca(X_norm)
    X = projectData(X_norm, U, 2)
    # last index defines the number of features to which X is to be projected which should be less than shape(X)[1]
    K = 6
    max_iters = 15
    initial_centroids = kMeansInitCentroids(X, K)
    centroids, idx = runkMeans(X, initial_centroids, max_iters, plot=True)
    numpy.savetxt('clustersprev.csv', idx, delimiter=',')

    ch = {}
    df = open('testing.txt')
    c = 0
    for item in df:
        ch[c] = int(float(item))
        c += 1
    ch = ch.values()
    ch = numpy.array(ch)
    numpy.savetxt('check.csv', ch, delimiter=',')

def main():
    kMeansClustering()

if __name__ == '__main__':
    main()