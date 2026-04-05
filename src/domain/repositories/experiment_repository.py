class ExperimentRepository:
    def save(self, experiment):
        raise NotImplementedError

    def get_by_id(self, id):
        raise NotImplementedError


class GenerationRepository:
    def save(self, generation, best_fitness):
        raise NotImplementedError

    def get_by_experiment(self, experiment_id):
        raise NotImplementedError


class IndividualRepository:
    def save(self, individual, generation_id):
        raise NotImplementedError

    def get_by_generation(self, generation_id):
        raise NotImplementedError


class SimulationRepository:
    def save(self, individual_id, result):
        raise NotImplementedError

    def get_by_individual(self, individual_id):
        raise NotImplementedError