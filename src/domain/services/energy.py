def compute_energy(individual, time):
    N = individual.rpm / 60
    Q = individual.flow
    T = individual.temperature

    T_amb = 25

    k1 = 0.1
    k2 = 1.0
    k3 = 0.05

    P_agit = k1 * (N ** 3)
    P_pump = k2 * Q
    P_temp = k3 * abs(T - T_amb)

    total_power = P_agit + P_pump + P_temp

    return total_power * time