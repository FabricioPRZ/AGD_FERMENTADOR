class GetBestPerGeneration:

    def __init__(self, experiment_repo, generation_repo, individual_repo):
        self.experiment_repo = experiment_repo
        self.generation_repo = generation_repo
        self.individual_repo = individual_repo

    def execute(self, experiment_id):
        experiment  = self.experiment_repo.get_by_id(experiment_id)
        generations = self.generation_repo.get_by_experiment(experiment_id)

        result = []

        for gen in generations:
            individuals = self.individual_repo.get_by_generation(gen.id)

            if not individuals:
                continue

            best = max(individuals, key=lambda x: x.fitness)

            result.append({
                "generation":  gen.number,
                "best_fitness": gen.best_fitness,
                "best_individual": {
                    "id":          best.id,
                    "rpm":         best.rpm,
                    "temperature": best.temperature,
                    "flow":        best.flow,
                    "fitness":     best.fitness,
                    "ethanol":     best.ethanol,
                    "biomass":     best.biomass,
                    "substrate":   best.substrate,
                    "efficiency":  best.efficiency,
                    "energy":      best.energy,
                }
            })

        return {
            "experiment_id": experiment_id,
            "generations":   result
        }