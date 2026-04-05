from application.use_cases.run_experiment import RunExperiment
from application.use_cases.get_experiment import GetExperiment
from application.use_cases.get_simulation import GetSimulation
from application.dto.experiment_input_dto import ExperimentInputDTO
from infrastructure.repositories.mysql_experiment_repository import MySQLExperimentRepository
from infrastructure.repositories.mysql_generation_repository import MySQLGenerationRepository
from infrastructure.repositories.mysql_individual_repository import MySQLIndividualRepository
from infrastructure.repositories.mysql_simulation_repository import MySQLSimulationRepository


class ExperimentController:

    def __init__(self):
        experiment_repo = MySQLExperimentRepository()
        generation_repo = MySQLGenerationRepository()
        individual_repo = MySQLIndividualRepository()
        simulation_repo = MySQLSimulationRepository()

        self.run_use_case = RunExperiment(
            experiment_repo=experiment_repo,
            generation_repo=generation_repo,
            individual_repo=individual_repo,
            simulation_repo=simulation_repo
        )
        self.get_use_case = GetExperiment(
            experiment_repo=experiment_repo,
            generation_repo=generation_repo,
            individual_repo=individual_repo,
            simulation_repo=simulation_repo
        )
        self.simulation_use_case = GetSimulation(
            simulation_repo=simulation_repo
        )

    def run(self, request):
        dto = ExperimentInputDTO(
            ph=request.ph,
            temperature=request.temperature,
            sugar=request.sugar,
            microorganism=request.microorganism,
            micro_amount=request.micro_amount
        )
        result = self.run_use_case.execute(dto)
        return {
            "experiment_id": result.experiment_id,
            "best_individual": {
                "rpm":         result.best_individual.rpm,
                "temperature": result.best_individual.temperature,
                "flow":        result.best_individual.flow,
                "fitness":     result.best_individual.fitness,
            },
            "history": result.history
        }

    def get_experiment(self, experiment_id):
        return self.get_use_case.execute(experiment_id)

    def get_simulation(self, individual_id):
        return self.simulation_use_case.execute(individual_id)