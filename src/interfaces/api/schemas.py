from pydantic import BaseModel


class ExperimentRequest(BaseModel):
    ph:           float
    temperature:  float
    sugar:        float
    microorganism: str
    micro_amount: float


class IndividualResponse(BaseModel):
    rpm:         float
    temperature: float
    flow:        float
    fitness:     float


class ExperimentResponse(BaseModel):
    best_individual: IndividualResponse
    history:         list[float]