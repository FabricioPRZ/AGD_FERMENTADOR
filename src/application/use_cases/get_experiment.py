class GetExperiment:

    def __init__(self, experiment_repo, generation_repo, individual_repo, simulation_repo):
        self.experiment_repo = experiment_repo
        self.generation_repo = generation_repo
        self.individual_repo = individual_repo
        self.simulation_repo = simulation_repo

    def execute(self, experiment_id):
        experiment  = self.experiment_repo.get_by_id(experiment_id)
        generations = self.generation_repo.get_by_experiment(experiment_id)

        result = []

        for gen in generations:
            individuals = self.individual_repo.get_by_generation(gen.id)

            inds_data = []
            for ind in individuals:
                inds_data.append({
                    "id":          ind.id,
                    "rpm":         ind.rpm,
                    "temperature": ind.temperature,
                    "flow":        ind.flow,
                    "fitness":     ind.fitness,
                    "ethanol":     ind.ethanol,
                    "biomass":     ind.biomass,
                    "substrate":   ind.substrate,
                    "efficiency":  ind.efficiency,
                    "energy":      ind.energy,
                })

            result.append({
                "generation":   gen.number,
                "best_fitness": gen.best_fitness,
                "individuals":  inds_data
            })

        return {
            "experiment": {
                "id":          experiment.id,
                "ph":          experiment.ph,
                "temperature": experiment.temperature,
                "sugar":       experiment.sugar
            },
            "generations": result
        }