from fastapi import APIRouter
from interfaces.api.schemas import ExperimentRequest
from interfaces.api.controllers import ExperimentController

router = APIRouter()
controller = ExperimentController()


@router.post("/run-experiment")
def run_experiment(request: ExperimentRequest):
    return controller.run(request)


@router.get("/experiment/{experiment_id}")
def get_experiment(experiment_id: str):
    return controller.get_experiment(experiment_id)


@router.get("/simulation/{individual_id}")
def get_simulation(individual_id: str):
    return controller.get_simulation(individual_id)