from infrastructure.database.connection import SessionLocal
from infrastructure.database.models import ExperimentModel
from domain.entities.experiment import Experiment


class MySQLExperimentRepository:

    def save(self, experiment):
        session = SessionLocal()
        try:
            db = ExperimentModel(
                id=experiment.id,
                ph=experiment.ph,
                initial_temperature=experiment.temperature,
                sugar_concentration=experiment.sugar,
                microorganism_type=experiment.microorganism,
                microorganism_amount=experiment.micro_amount,
                status="completed"
            )
            session.add(db)
            session.commit()
        finally:
            session.close()

    def get_by_id(self, id):
        session = SessionLocal()
        try:
            db = session.query(ExperimentModel).filter(ExperimentModel.id == id).first()
            if not db:
                return None
            return Experiment(
                id=db.id,
                ph=db.ph,
                temperature=db.initial_temperature,
                sugar=db.sugar_concentration,
                microorganism=db.microorganism_type,
                micro_amount=db.microorganism_amount
            )
        finally:
            session.close()