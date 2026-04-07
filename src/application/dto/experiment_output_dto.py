class ExperimentOutputDTO:
    def __init__(self, experiment_id, best_individual, history, history_worst, history_avg):
        self.experiment_id   = experiment_id
        self.best_individual = best_individual
        self.history         = history
        self.history_worst   = history_worst
        self.history_avg     = history_avg