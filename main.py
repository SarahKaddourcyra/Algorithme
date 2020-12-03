import math
import time
from aco import ACO, Graph
from plot import plot
#import numpy as np

def distance(city1: dict, city2: dict):
    return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)


def main():
    cities = []
    points = []
    with open('./data/ulysses16.tsp') as f:
        for line in f.readlines():
            #print(line)
            city = line.split(' ')
            #print(city)
            cities.append(dict(index=float(city[0]), x=float(city[1]), y=float(city[2])))
            #print(cities)
            points.append((float(city[1]), float(city[2])))
    cost_matrix = []
    rank = len(cities)
    #print(rank)
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(distance(cities[i], cities[j]))
        cost_matrix.append(row)
    #print('cost_matrix',cost_matrix)
    aco = ACO(100,1, 1.0, 10.0, 0.5, 10, 2)
    graph = Graph(cost_matrix, rank)
    path, cost = aco.solve(graph)
    cost=cost+cost_matrix[path[-2]][path[-1]]
    print('cost: {}, path: {}'.format(cost, path))
    plot(points, path)
if __name__ == '__main__':
    debut=time.time()
    main()
    fin=time.time()
    print('le temps d execution=',fin-debut)
