from .energy import compute_energy

def compute_fitness(result, individual):
    ethanol = result["ethanol"][-1]
    substrate_initial = result["substrate"][0]
    substrate_final = result["substrate"][-1]

    sugar_used = substrate_initial - substrate_final

    if sugar_used <= 0:
        return 0

    theoretical = sugar_used * 0.5
    efficiency = min(ethanol / theoretical, 1.0)

    time_total = result["time"][-1]
    energy = compute_energy(individual, time_total)

    energy_norm = energy / 1000
    alpha = 0.3

    individual.energy = energy
    individual.efficiency = efficiency

    return efficiency - alpha * energy_norm