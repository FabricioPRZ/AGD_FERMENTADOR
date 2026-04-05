from sqlalchemy import Column, String, Float, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class ExperimentModel(Base):
    __tablename__ = "experiments"

    id                   = Column(String(36), primary_key=True)
    name                 = Column(String(100))
    ph                   = Column(Float)
    initial_temperature  = Column(Float)
    sugar_concentration  = Column(Float)
    microorganism_type   = Column(String(100))
    microorganism_amount = Column(Float)
    total_time           = Column(Float, default=200)
    status               = Column(String(20))
    execution_time       = Column(Float)
    created_at           = Column(TIMESTAMP, default=datetime.utcnow)

    generations = relationship("GenerationModel", back_populates="experiment")


class GenerationModel(Base):
    __tablename__ = "generations"

    id                = Column(String(36), primary_key=True)
    experiment_id     = Column(String(36), ForeignKey("experiments.id"))
    generation_number = Column(Integer)
    best_fitness      = Column(Float)

    experiment  = relationship("ExperimentModel", back_populates="generations")
    individuals = relationship("IndividualModel", back_populates="generation")


class IndividualModel(Base):
    __tablename__ = "individuals"

    id                 = Column(String(36), primary_key=True)
    generation_id      = Column(String(36), ForeignKey("generations.id"))
    rpm                = Column(Float)
    temperature        = Column(Float)
    flow               = Column(Float)
    fitness            = Column(Float)
    final_ethanol      = Column(Float)
    final_biomass      = Column(Float)
    final_substrate    = Column(Float)
    efficiency         = Column(Float)
    energy_consumption = Column(Float)

    generation          = relationship("GenerationModel", back_populates="individuals")
    simulation_results  = relationship("SimulationResultModel", back_populates="individual")


class SimulationResultModel(Base):
    __tablename__ = "simulation_results"

    id            = Column(String(36), primary_key=True)
    individual_id = Column(String(36), ForeignKey("individuals.id"))
    time          = Column(Float)
    biomass       = Column(Float)
    substrate     = Column(Float)
    ethanol       = Column(Float)

    individual = relationship("IndividualModel", back_populates="simulation_results")