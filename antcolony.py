from ant import Ant
from threading import Lock, Condition

import random
import sys

class AntColony:
    def __init__(self, graph, num_ants, num_iterations):
        self.graph = graph
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.Alpha = 0.1

        # Змінна умови
        self.cv = Condition()
        self.reset()

    def reset(self):
        self.best_path_cost = sys.maxsize
        self.best_path_vec = None
        self.best_path_mat  = None
        self.last_best_path_iteration = 0

    def start(self):
        self.ants = self.create_ants()
        self.iter_counter = 0

        while self.iter_counter < self.num_iterations:
            self.iteration()

            self.cv.acquire()
            # очікування доки оновлення не викличе метод notify()
            self.cv.wait()

            lock = self.graph.lock
            lock.acquire()
            self.global_updating_rule()
            lock.release()

            self.cv.release()

    # одна ітерація включає генерацію числа мурашиних потоків
    def iteration(self):
        self.avg_path_cost = 0
        self.ant_counter = 0
        self.iter_counter += 1
        print("iter_counter = %s" % (self.iter_counter,))
        for ant in self.ants:
            print("starting ant = %s" % (ant.ID))
            ant.start()

    def num_ants(self):
        return len(self.ants)

    def num_iterations(self):
        return self.num_iterations

    def iteration_counter(self):
        return self.iter_counter

    # викликається окремими мурахами
    def update(self, ant):
        lock = Lock()
        lock.acquire()
        print ("Update called by %s" % (ant.ID,))
        self.ant_counter += 1
        self.avg_path_cost += ant.path_cost
        if ant.path_cost < self.best_path_cost:
            self.best_path_cost = ant.path_cost
            self.best_path_mat = ant.path_mat
            self.best_path_vec = ant.path_vec
            self.last_best_path_iteration = self.iter_counter

        if self.ant_counter == len(self.ants):
            self.avg_path_cost /= len(self.ants)
            print ("Best: %s, %s, %s, %s" % (self.best_path_vec, self.best_path_cost, self.iter_counter, self.avg_path_cost,))
            self.cv.acquire()
            self.cv.notify()
            self.cv.release()

    def done(self):
        return self.iter_counter == self.num_iterations

    # присвоєння кожній мурасі випадково обрану вершину
    def create_ants(self):
        self.reset()
        ants = []
        for i in range(0, self.num_ants):
            ant = Ant(i, random.randint(0, self.graph.num_nodes - 1), self)
            ants.append(ant)
        return ants

    # зміна матриці відстаней (tau) відповідно до випаровування і насаджування (evaporation/deposition)
    def global_updating_rule(self):
        for r in range(0, self.graph.num_nodes):
            for s in range(0, self.graph.num_nodes):
                if r != s:
                    delt_tau = self.best_path_mat[r][s] / self.best_path_cost
                    evaporation = (1 - self.Alpha) * self.graph.tau(r, s)
                    deposition = self.Alpha * delt_tau

                    self.graph.update_tau(r, s, evaporation + deposition)
