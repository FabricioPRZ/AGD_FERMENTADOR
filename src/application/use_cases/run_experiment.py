import uuid
import random
from domain.entities.experiment import Experiment
from domain.entities.generation import Generation
from domain.services.genetic_algorithm import GeneticAlgorithm
from application.dto.experiment_output_dto import ExperimentOutputDTO

class RunExperiment:

    def __init__(self, experiment_repo, generation_repo, individual_repo, simulation_repo):
        self.experiment_repo = experiment_repo
        self.generation_repo = generation_repo
        self.individual_repo = individual_repo
        self.simulation_repo = simulation_repo

    def execute(self, input_dto):

        experiment = Experiment(
            id=str(uuid.uuid4()),
            ph=input_dto.ph,
            temperature=input_dto.temperature,
            sugar=input_dto.sugar,
            microorganism=input_dto.microorganism,
            micro_amount=input_dto.micro_amount
        )
        self.experiment_repo.save(experiment)

        initial_conditions = {
            "biomass":              input_dto.micro_amount,
            "sugar":                input_dto.sugar,
            "ph":                   input_dto.ph,
            "temperature":          input_dto.temperature,
            "microorganism":        input_dto.microorganism,
            "microorganism_amount": input_dto.micro_amount
        }

        ga = GeneticAlgorithm()
        population = [ga.create_individual() for _ in range(ga.pop_size)]
        history       = []
        history_worst = []
        history_avg   = []

        for gen_number in range(ga.max_generations):
            ga.evaluate(population, initial_conditions)

            best  = max(population, key=lambda x: x.fitness)
            worst = min(population, key=lambda x: x.fitness)
            avg   = sum(ind.fitness for ind in population) / len(population)

            history.append(best.fitness)
            history_worst.append(worst.fitness)
            history_avg.append(avg)

            generation = Generation(
                id=None,
                number=gen_number,
                experiment_id=experiment.id
            )
            generation_id = self.generation_repo.save(generation, best.fitness)

            best_ind_id = None
            for ind in population:
                ind_id = self.individual_repo.save(ind, generation_id)
                if ind.fitness == best.fitness:
                    best_ind_id = ind_id

            if best_ind_id:
                self.simulation_repo.save(best_ind_id, best.simulation_result)

            if ga.has_converged(history):
                print(f"Convergió en generación {gen_number}")
                break

            selected = ga.select(population)
            new_pop = []
            while len(new_pop) < ga.pop_size:
                p1, p2 = random.sample(selected, 2)
                child = ga.crossover(p1, p2)
                child = ga.mutate(child)
                new_pop.append(child)
            population = new_pop

        ga.evaluate(population, initial_conditions)
        best = max(population, key=lambda x: x.fitness)

        return ExperimentOutputDTO(experiment.id, best, history, history_worst, history_avg)