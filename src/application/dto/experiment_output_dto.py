class ExperimentOutputDTO:
    def __init__(self, experiment_id, best_individual, history):
        self.experiment_id   = experiment_id
        self.best_individual = best_individual
        self.history         = history