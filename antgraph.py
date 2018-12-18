from threading import Lock

class AntGraph:
    def __init__(self, num_nodes, delta_mat, tau_mat=None):
        if len(delta_mat) != num_nodes:
            raise Exception("len(delta) != num_nodes")

        self.num_nodes = num_nodes
        # Матриця відстаней між вершинами (deltas)
        self.delta_mat = delta_mat
        self.lock = Lock()

        # Матриця tau містить величину феромону на вершині x,y
        if tau_mat is None:
            self.tau_mat = []
            for i in range(0, num_nodes):
                self.tau_mat.append([0]*num_nodes)

    def delta(self, r, s):
        return self.delta_mat[r][s]

    def tau(self, r, s):
        return self.tau_mat[r][s]

    # 1 / delta = eta або "зір" мурахи
    def etha(self, r, s):
        return 1.0 / float(self.delta(r, s))

    # внутрішні замки (locks) , швидше за все, не потрібні
    def update_tau(self, r, s, val):
        self.tau_mat[r][s] = val


    def reset_tau(self):
        lock = Lock()
        lock.acquire()
        avg = self.average_delta()

        # початкове значення феромону
        self.tau0 = 1.0 / (self.num_nodes * 0.5 * avg)


        for r in range(0, self.num_nodes):
            for s in range(0, self.num_nodes):
                self.tau_mat[r][s] = self.tau0
        lock.release()

    # Середнє значення відстані в матриці відстаней
    def average_delta(self):
        sum = 0
        matrix = self.delta_mat
        for r in range(0, self.num_nodes):
            for s in range(0, self.num_nodes):
                sum += matrix[r][s]

        avg = sum / (self.num_nodes * self.num_nodes)
        return avg

