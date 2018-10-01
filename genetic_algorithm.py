import chess
from random import SystemRandom
from copy import deepcopy
import pickle


class GA:
    def __init__(self, n_pop, prob, board):
        self.__population = []
        self.__pop_fit = []
        for i in range(n_pop):
            self.__population.append(board.new_random_state())
        self.__probability = prob
        self.__n_pop = n_pop
        self.__randomizer = SystemRandom()

    @property
    def size(self):
        return self.__n_pop

    @property
    def population(self):
        return self.__population

    @property
    def probability(self):
        return self.__probability

    @property
    def randomizer(self):
        return self.__randomizer

    # Enumerate all fitness point in population
    def calc_all_fit(self):
        self.__pop_fit = []
        for board in self.population:
            ff, kill = board.count_total_targets()
            self.__pop_fit.append(kill - ff)
        min_score = min(self.__pop_fit)
        for i in range(len(self.__pop_fit)):
            self.__pop_fit[i] += abs(min_score)

    # return board with higher fitness point in population
    def best_board(self):
        idx = self.__pop_fit.index(max(self.__pop_fit))
        return self.population[idx]

    def mutate(self, board):
        p = self.randomizer.random()
        if (p < self.probability / 100):
            while True:
                mask = self.randomizer.randint(0, (1 << board.size) - 1)
                # max pieces mutated up to 3 pieces
                if (bin(mask).count("1") < 4):
                    break
            for i in range(board.size):
                if (mask & (1 << i)):
                    board.pieces[i].random_move()
        board.conflict_resolve()
        return board

    def crossover(self, board1, board2):
        mask = self.randomizer.randint(0, (1 << board1.size) - 1)
        new_board1 = chess.Board(board1.size)
        new_board2 = chess.Board(board1.size)
        for i in range(new_board1.size):
            if (mask & (1 << i)):
                # new_board1.add_piece(deepcopy(board2.pieces[i]))
                # new_board2.add_piece(deepcopy(board1.pieces[i]))
                new_board1.add_piece(pickle.loads(
                    pickle.dumps((board2.pieces[i]))))
                new_board2.add_piece(pickle.loads(
                    pickle.dumps((board1.pieces[i]))))
                # set new board reference
                new_board1.pieces[-1].board = new_board1
                new_board2.pieces[-1].board = new_board2
            else:
                # new_board1.add_piece(deepcopy(board1.pieces[i]))
                # new_board2.add_piece(deepcopy(board2.pieces[i]))
                new_board1.add_piece(pickle.loads(
                    pickle.dumps((board1.pieces[i]))))
                new_board2.add_piece(pickle.loads(
                    pickle.dumps((board2.pieces[i]))))
                # set new board reference
                new_board1.pieces[-1].board = new_board1
                new_board2.pieces[-1].board = new_board2
        return new_board1, new_board2

    # return random board using fitness point
    def random_parent(self):
        return self.randomizer.choices(self.population, self.__pop_fit)[0]

    def do_algorithm(self, n_iter):
        for i in range(n_iter):
            print("Generation %d" % (i + 1))

            self.calc_all_fit()
            temp_population = []

            while (len(temp_population) < self.size):
                parent1 = self.random_parent()
                parent2 = self.random_parent()

                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                temp_population.append(child1)
                temp_population.append(child2)

            self.__population = temp_population
        self.calc_all_fit()


if __name__ == '__main__':
    b = chess.Board(8)
    # b.random_fill(8)
    b.fill_piece_from_file(8)
    print("Initial Genetic Algorithm (ff, kill):", b.count_total_targets())
    print(b)

    g = GA(50, 10, b)
    g.do_algorithm(30)

    z = g.best_board()
    print("Genetic Algorithm (ff, kill):", z.count_total_targets())
    print(z)
