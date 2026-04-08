import numpy as np
from scipy.integrate import odeint


def simulate(individual, initial_conditions):
    rpm = individual.rpm
    temp = individual.temperature
    flow = individual.flow

    X0 = initial_conditions["biomass"]
    S0 = initial_conditions["sugar"]
    E0 = 0

    ph_factor = 1.0 - abs(initial_conditions["ph"] - 5.5) * 0.1
    micro_factor = initial_conditions["microorganism_amount"]

    mu = 0.04 * (temp / 30) * (rpm / 100) * ph_factor * micro_factor
    Xm = 8

    k1 = 0.5 * (rpm / 100)
    k2 = 0.3 * (flow / 10)

    def model(y, t):
        X, S, E = y
        S = max(S, 0)
        X = max(X, 0)
        dXdt = mu * X * (1 - X / Xm)
        dSdt = -k1 * X if S > 0 else 0
        dEdt = k2 * X
        return [dXdt, dSdt, dEdt]

    t = np.linspace(0, 120, 200)
    sol = odeint(model, [X0, S0, E0], t)

    biomass   = np.clip(np.nan_to_num(sol[:, 0], nan=0.0, posinf=0.0, neginf=0.0), 0, 1e6)
    substrate = np.clip(np.nan_to_num(sol[:, 1], nan=0.0, posinf=0.0, neginf=0.0), 0, 1e6)
    ethanol   = np.clip(np.nan_to_num(sol[:, 2], nan=0.0, posinf=0.0, neginf=0.0), 0, 1e6)

    return {
        "time":      t,
        "biomass":   biomass,
        "substrate": substrate,
        "ethanol":   ethanol
    }