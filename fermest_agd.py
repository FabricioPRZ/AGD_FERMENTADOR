import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# ==============================
# CONFIGURACIÓN INICIAL
# ==============================

initial_conditions = {
    "biomass": 0.15,
    "sugar": 100,
    "ph": 5.5,
    "temperature": 30,
    "microorganism": "yeast",
    "microorganism_amount": 0.15
}

# ==============================
# SIMULADOR DINÁMICO
# ==============================

def simulate(individual, initial_conditions):
    rpm = individual["rpm"]
    temp = individual["temperature"]
    flow = individual["flow"]

    X0 = initial_conditions["biomass"]
    S0 = initial_conditions["sugar"]
    E0 = 0
    y0 = [X0, S0, E0]

    # Ajustes por condiciones iniciales
    ph_factor = 1.0 - abs(initial_conditions["ph"] - 5.5) * 0.1
    micro_factor = initial_conditions["microorganism_amount"]

    # Parámetros dinámicos
    mu = 0.04 * (temp / 30) * (rpm / 100) * ph_factor * micro_factor
    Xm = 8

    k1 = 0.5 * (rpm / 100)
    k2 = 0.3 * (flow / 10)

    def model(y, t):
        X, S, E = y
        
        dXdt = mu * X * (1 - X/Xm)
        dSdt = -k1 * X
        dEdt = k2 * X
        
        return [dXdt, dSdt, dEdt]

    t = np.linspace(0, 200, 200)
    sol = odeint(model, y0, t)

    X = sol[:, 0]
    S = sol[:, 1]
    E = sol[:, 2]

    return {
        "time": t,
        "biomass": X,
        "substrate": S,
        "ethanol": E,
        "final_ethanol": E[-1],
        "final_substrate": S[-1],
        "initial_substrate": S0
    }

# ==============================
# FUNCIÓN FITNESS
# ==============================

def fitness(result, individual):
    ethanol = result["final_ethanol"]
    sugar_used = result["initial_substrate"] - result["final_substrate"]

    if sugar_used <= 0:
        return 0

    theoretical = sugar_used * 0.5
    efficiency = ethanol / theoretical

    # Penalización energética
    energy_penalty = (
        individual["rpm"] * 0.01 +
        individual["flow"] * 0.05 +
        individual["temperature"] * 0.01
    )

    return efficiency - energy_penalty

# ==============================
# ALGORITMO GENÉTICO
# ==============================

def create_individual():
    return {
        "rpm": random.uniform(50, 200),
        "temperature": random.uniform(20, 40),
        "flow": random.uniform(1, 10),
        "fitness": None
    }

def evaluate_population(pop, initial_conditions):
    for ind in pop:
        result = simulate(ind, initial_conditions)
        ind["fitness"] = fitness(result, ind)

def selection(pop):
    pop = sorted(pop, key=lambda x: x["fitness"], reverse=True)
    return pop[:len(pop)//2]

def crossover(p1, p2):
    return {
        "rpm": (p1["rpm"] + p2["rpm"]) / 2,
        "temperature": (p1["temperature"] + p2["temperature"]) / 2,
        "flow": (p1["flow"] + p2["flow"]) / 2,
        "fitness": None
    }

def mutate(ind):
    if random.random() < 0.2:
        ind["rpm"] += random.uniform(-10, 10)
    if random.random() < 0.2:
        ind["temperature"] += random.uniform(-2, 2)
    if random.random() < 0.2:
        ind["flow"] += random.uniform(-1, 1)

    # límites físicos
    ind["rpm"] = max(10, min(ind["rpm"], 300))
    ind["temperature"] = max(10, min(ind["temperature"], 50))
    ind["flow"] = max(0.1, min(ind["flow"], 20))

    return ind

def genetic_algorithm(initial_conditions, generations=20, pop_size=20):
    population = [create_individual() for _ in range(pop_size)]
    history = []

    for gen in range(generations):
        evaluate_population(population, initial_conditions)

        best = max(population, key=lambda x: x["fitness"])
        history.append(best["fitness"])

        print(f"Gen {gen} | Best fitness: {best['fitness']:.4f}")

        selected = selection(population)

        offspring = []
        while len(offspring) < pop_size:
            p1, p2 = random.sample(selected, 2)
            child = crossover(p1, p2)
            child = mutate(child)
            offspring.append(child)

        population = offspring

    evaluate_population(population, initial_conditions)
    best = max(population, key=lambda x: x["fitness"])

    return best, history

# ==============================
# GRÁFICAS
# ==============================

def plot_results(best, history, initial_conditions):
    result = simulate(best, initial_conditions)

    # Curvas de fermentación
    plt.figure()
    plt.plot(result["time"], result["biomass"], label="Biomasa")
    plt.plot(result["time"], result["substrate"], label="Sustrato")
    plt.plot(result["time"], result["ethanol"], label="Etanol")
    plt.xlabel("Tiempo")
    plt.ylabel("Concentración")
    plt.title("Mejor individuo")
    plt.legend()
    plt.grid()

    # Evolución del fitness
    plt.figure()
    plt.plot(history)
    plt.xlabel("Generación")
    plt.ylabel("Fitness")
    plt.title("Evolución del algoritmo genético")
    plt.grid()

    plt.show()

# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    best, history = genetic_algorithm(initial_conditions)

    print("\n===== MEJOR SOLUCIÓN =====")
    print(f"RPM: {best['rpm']:.2f}")
    print(f"Temperatura: {best['temperature']:.2f}")
    print(f"Caudal: {best['flow']:.2f}")
    print(f"Fitness: {best['fitness']:.4f}")

    plot_results(best, history, initial_conditions)