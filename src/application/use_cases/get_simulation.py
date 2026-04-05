class GetSimulation:

    def __init__(self, simulation_repo):
        self.simulation_repo = simulation_repo

    def execute(self, individual_id):
        return self.simulation_repo.get_by_individual(individual_id)