class Individual:
    def __init__(self, rpm, temperature, flow):
        self.id = None
        self.rpm = rpm
        self.temperature = temperature
        self.flow = flow

        self.fitness = None
        self.ethanol = None
        self.substrate = None
        self.biomass = None
        self.energy = None
        self.efficiency = None
        self.simulation_result = None