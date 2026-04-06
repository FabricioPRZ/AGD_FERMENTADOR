import random

from domain.entities.individual import Individual
from domain.services.simulator import simulate
from domain.services.fitness import compute_fitness


class GeneticAlgorithm:

    def __init__(self, pop_size=20, max_generations=50, patience=5, threshold=0.001):
        self.pop_size = pop_size
        self.max_generations = max_generations
        self.patience = patience
        self.threshold = threshold

    def create_individual(self):
        return Individual(
            rpm=random.uniform(50, 200),
            temperature=random.uniform(20, 40),
            flow=random.uniform(1, 10)
        )

    def evaluate(self, population, initial_conditions):
        for ind in population:
            result = simulate(ind, initial_conditions)
            ind.fitness = compute_fitness(result, ind)
            ind.ethanol = result["ethanol"][-1]
            ind.biomass = result["biomass"][-1]
            ind.substrate = result["substrate"][-1]
            ind.simulation_result = result

    def select(self, population):
        population.sort(key=lambda x: x.fitness, reverse=True)
        return population[:len(population) // 2]

    def crossover(self, p1, p2):
        return Individual(
            rpm=(p1.rpm + p2.rpm) / 2,
            temperature=(p1.temperature + p2.temperature) / 2,
            flow=(p1.flow + p2.flow) / 2
        )

    def mutate(self, ind):
        if random.random() < 0.2:
            ind.rpm += random.uniform(-10, 10)
        if random.random() < 0.2:
            ind.temperature += random.uniform(-2, 2)
        if random.random() < 0.2:
            ind.flow += random.uniform(-1, 1)

        ind.rpm = max(50, min(ind.rpm, 200))
        ind.temperature = max(20, min(ind.temperature, 40))
        ind.flow = max(1, min(ind.flow, 10))
        
        return ind

    def has_converged(self, history):
        if len(history) < self.patience:
            return False
        recent = history[-self.patience:]
        return max(recent) - min(recent) < self.threshold

    def run(self, initial_conditions):
        population = [self.create_individual() for _ in range(self.pop_size)]
        history = []

        for gen in range(self.max_generations):
            self.evaluate(population, initial_conditions)
            best = max(population, key=lambda x: x.fitness)
            history.append(best.fitness)

            if self.has_converged(history):
                print(f"Convergió en generación {gen}")
                break

            selected = self.select(population)

            new_pop = []
            while len(new_pop) < self.pop_size:
                p1, p2 = random.sample(selected, 2)
                child = self.crossover(p1, p2)
                child = self.mutate(child)
                new_pop.append(child)

            population = new_pop

        self.evaluate(population, initial_conditions)
        return max(population, key=lambda x: x.fitness), history