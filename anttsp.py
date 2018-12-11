from antcolony import AntColony
from antgraph import AntGraph

import matplotlib.pyplot as plt


import sys
import traceback
import xlrd
import time

start_time = time.time()

#default
print('How many cities?')
num_nodes = int(input())

print('How many ants?')
num_ants = int(input())

print('How long life of colony (iterations)?')
num_iterations = int(input())

num_repetitions = 1
num_iterations=1

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1]:
        num_nodes = int(sys.argv[1])

    workbook = xlrd.open_workbook('Data.xlsx')
    ws = workbook.sheet_by_index(0)

    cities, cost_mat = [], []
    x_data, y_data = [], []
    graph_x_cords, graph_y_cords = [], []
    for row in range(1, ws.nrows):
        cities.append(ws.cell_value(row, 1))

    for col in range(2, ws.ncols-2):
        cost_mat.append([])
        for row in range(1, ws.nrows):
            cost_mat[col-2].append(ws.cell_value(row, col))

    for row in range(1, ws.nrows):
        x_data.append(ws.cell_value(row, ws.ncols - 2))

    for row in range(1, ws.nrows):
        y_data.append(ws.cell_value(row, ws.ncols - 1))

    if num_nodes < len(cost_mat):
        cost_mat = cost_mat[0:num_nodes]
        for i in range(0, num_nodes):
            cost_mat[i] = cost_mat[i][0:num_nodes]

    try:
        graph = AntGraph(num_nodes, cost_mat)
        best_path_vec = None
        best_path_cost = sys.maxsize

        for i in range(0, num_repetitions):
            graph.reset_tau()
            ant_colony = AntColony(graph, num_ants, num_iterations)
            ant_colony.start()
            if ant_colony.best_path_cost < best_path_cost:
                best_path_vec = ant_colony.best_path_vec
                best_path_cost = ant_colony.best_path_cost

        print ("                     Results                                ")
        print ("\nBest path = %s" % (best_path_vec,))
        for node in best_path_vec:
            print (cities[node] + " ",)
            graph_x_cords.append(float(x_data[node]))
            graph_y_cords.append(float(y_data[node]))

        print ("\nBest path cost = %s\n" % (best_path_cost,))

        print("--- %s seconds ---" % (time.time() - start_time))

        graph_x_cords.append(graph_x_cords[0])
        graph_y_cords.append(graph_y_cords[0])

        plt.plot(graph_x_cords, graph_y_cords, color='green', linestyle='dashed', linewidth=3,
                 marker='o', markerfacecolor='blue', markersize=12)

        for node in best_path_vec:
            city = cities[node]
            plt.annotate(f'{city}', (float(x_data[node]), float(y_data[node])),xytext=(8, 2.95), textcoords='offset points')
        plt.show()

    except :
        print("exception: " )
        traceback.print_exc()

