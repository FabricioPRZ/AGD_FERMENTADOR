import uuid

from infrastructure.database.connection import SessionLocal
from infrastructure.database.models import IndividualModel
from domain.entities.individual import Individual


class MySQLIndividualRepository:

    def save(self, individual, generation_id):
        session = SessionLocal()
        try:
            db = IndividualModel(
                id=str(uuid.uuid4()),
                generation_id=generation_id,
                rpm=individual.rpm,
                temperature=individual.temperature,
                flow=individual.flow,
                fitness=individual.fitness,
                final_ethanol=individual.ethanol,
                final_biomass=individual.biomass,
                final_substrate=individual.substrate,
                efficiency=individual.efficiency,
                energy_consumption=individual.energy
            )
            session.add(db)
            session.commit()
            return db.id
        finally:
            session.close()

    def get_by_generation(self, generation_id):
        session = SessionLocal()
        try:
            rows = (
                session.query(IndividualModel)
                .filter(IndividualModel.generation_id == generation_id)
                .all()
            )
            individuals = []
            for r in rows:
                ind = Individual(rpm=r.rpm, temperature=r.temperature, flow=r.flow)
                ind.id        = r.id
                ind.fitness   = r.fitness
                ind.ethanol   = r.final_ethanol
                ind.biomass   = r.final_biomass
                ind.substrate = r.final_substrate
                ind.efficiency = r.efficiency
                ind.energy    = r.energy_consumption
                individuals.append(ind)
            return individuals
        finally:
            session.close()