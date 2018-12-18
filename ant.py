import math
import random
from threading import *

class Ant(Thread):
    def __init__(self, ID, start_node, colony):
        Thread.__init__(self)
        self.ID = ID
        self.start_node = start_node
        self.colony = colony
        self.curr_node = self.start_node
        self.graph = self.colony.graph
        self.path_vec = []
        self.path_vec.append(self.start_node)
        self.path_cost = 0

        # Стандартні константні параметри
        self.Beta = 1
        self.Q0 = 0.5
        self.Rho = 0.99

        # Зберігаються вузли які ще не відвідані
        self.nodes_to_visit = {}

        for i in range(0, self.graph.num_nodes):
            if i != self.start_node:
                self.nodes_to_visit[i] = i

        # Створює нульову матрицю розміру n X n
        self.path_mat = []

        for i in range(0, self.graph.num_nodes):
            self.path_mat.append([0]*self.graph.num_nodes)

    # Переписуємо Thread's run()
    def run(self):
        graph = self.colony.graph
        while not self.end():
            # Необхідний винятковий доступ до графу
            graph.lock.acquire()
            new_node = self.state_transition_rule(self.curr_node)
            self.path_cost += graph.delta(self.curr_node, new_node)

            self.path_vec.append(new_node)
            # Матриця суміжності, що представляє шлях
            self.path_mat[self.curr_node][new_node] = 1

            
            self.local_updating_rule(self.curr_node, new_node)
            graph.lock.release()

            self.curr_node = new_node

        # Не забути замкнути маршрут
        self.path_cost += graph.delta(self.path_vec[-1], self.path_vec[0])

        # Передача результатів мурахи до колонії
        self.colony.update(self)

        # дозволяє потоку перезапускатись (викликає Thread.__init__)
        self.__init__(self.ID, self.start_node, self.colony)

    def end(self):
        return not self.nodes_to_visit 

    # визначає наступну верщину яка буде викликатись після поточної вершини (curr_node)
    def state_transition_rule(self, curr_node):
        graph = self.colony.graph
        start = random.random()
        max_node = -1

        if start < self.Q0:
            max_val = -1

            for node in self.nodes_to_visit.values():
                if graph.tau(curr_node, node) == 0:
                    raise Exception("tau = 0")

                val = graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)
                if val > max_val:
                    max_val = val
                    max_node = node
        else:
            sum = 0
            node = -1

            for node in self.nodes_to_visit.values():
                if graph.tau(curr_node, node) == 0:
                    raise Exception("tau = 0")
                sum += graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)
            if sum == 0:
                raise Exception("sum = 0")

            avg = sum / len(self.nodes_to_visit)


            for node in self.nodes_to_visit.values():
                p = graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta) 
                if p > avg:
                    max_node = node

            if max_node == -1:
                max_node = node
        
        if max_node < 0:
            raise Exception("max_node < 0")
        del self.nodes_to_visit[max_node]
        return max_node

    # оновлення феромону окремою мурахою
    def local_updating_rule(self, curr_node, next_node):
        graph = self.colony.graph
        val = (1 - self.Rho) * graph.tau(curr_node, next_node) + (self.Rho * graph.tau0)
        graph.update_tau(curr_node, next_node, val)

