from antcolony import AntColony
from antgraph import AntGraph

import matplotlib.pyplot as plt


import sys
import traceback
import xlrd
import time

# num_nodes = int(input('Скільки вершин?\n'))
# if num_nodes != '0':
#     num_ants = int(input('Скільки мурах в одній колонії (10 - 300) ?\n'))
#     num_iterations = int(input('Яка довжина життя колонії (кількість ітерацій 10 - 1000)?\n'))
# else:
num_nodes = 20
num_ants = 20
num_iterations = 30
# else:
#     num_ants = 40
#     num_iterations = 50


start_time = time.time()
# workbook = xlrd.open_workbook('Дані_Обл_Центри.xlsx')
workbook = xlrd.open_workbook('Дані_Lviv_Hub_ant.xlsx')
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
    num_repetitions = 1
    for i in range(0, num_repetitions):
        graph.reset_tau()
        ant_colony = AntColony(graph, num_ants, num_iterations)
        ant_colony.start()
        if ant_colony.best_path_cost < best_path_cost:
            best_path_vec = ant_colony.best_path_vec
            best_path_cost = ant_colony.best_path_cost
    print ("\n                     Результати                                ")
    print ("Вектор найкращого шляху = %s" % (best_path_vec,))
    for node in best_path_vec:
        print (str(cities[node]) + " ",)
        graph_x_cords.append(float(x_data[node]))
        graph_y_cords.append(float(y_data[node]))

    print ("Довжина найкращого шляху = %s\n" % (best_path_cost,))


    graph_x_cords.append(graph_x_cords[0])
    graph_y_cords.append(graph_y_cords[0])

    plt.plot(graph_x_cords, graph_y_cords, color='green', linestyle='dashed', linewidth=3,
                 marker='o', markerfacecolor='blue', markersize=12)

    for node in best_path_vec:
        city = cities[node]
        plt.annotate(f'{city}', (float(x_data[node]), float(y_data[node])),xytext=(8, 2.95), textcoords='offset points')
    plt.show()

    print("--- Тривалість дії алгоритму %s seconds ---" % (time.time() - start_time))
except :
    print("exception: " )
    traceback.print_exc()

