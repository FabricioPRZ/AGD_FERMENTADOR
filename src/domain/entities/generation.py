class Generation:
    def __init__(self, id, number, experiment_id, best_fitness=None):
        self.id = id
        self.number = number
        self.experiment_id = experiment_id
        self.best_fitness = best_fitness
        self.individuals = []