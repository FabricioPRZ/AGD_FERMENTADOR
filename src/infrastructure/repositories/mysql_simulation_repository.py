import uuid

from infrastructure.database.connection import SessionLocal
from infrastructure.database.models import SimulationResultModel


class MySQLSimulationRepository:

    def save(self, individual_id, result):
        session = SessionLocal()
        try:
            for i in range(len(result["time"])):
                db = SimulationResultModel(
                    id=str(uuid.uuid4()),
                    individual_id=individual_id,
                    time=float(result["time"][i]),
                    biomass=float(result["biomass"][i]),
                    substrate=float(result["substrate"][i]),
                    ethanol=float(result["ethanol"][i])
                )
                session.add(db)
            session.commit()
        finally:
            session.close()

    def get_by_individual(self, individual_id):
        session = SessionLocal()
        try:
            rows = (
                session.query(SimulationResultModel)
                .filter(SimulationResultModel.individual_id == individual_id)
                .order_by(SimulationResultModel.time)
                .all()
            )
            return {
                "time":      [r.time for r in rows],
                "biomass":   [r.biomass for r in rows],
                "substrate": [r.substrate for r in rows],
                "ethanol":   [r.ethanol for r in rows],
            }
        finally:
            session.close()