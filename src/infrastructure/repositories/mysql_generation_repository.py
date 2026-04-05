import uuid

from sqlalchemy.orm import joinedload
from infrastructure.database.connection import SessionLocal
from infrastructure.database.models import GenerationModel
from domain.entities.generation import Generation


class MySQLGenerationRepository:

    def save(self, generation, best_fitness):
        session = SessionLocal()
        try:
            db = GenerationModel(
                id=str(uuid.uuid4()),
                experiment_id=generation.experiment_id,
                generation_number=generation.number,
                best_fitness=best_fitness
            )
            session.add(db)
            session.commit()
            return db.id
        finally:
            session.close()

    def get_by_experiment(self, experiment_id):
        session = SessionLocal()
        try:
            rows = (
                session.query(GenerationModel)
                .options(joinedload(GenerationModel.individuals))
                .filter(GenerationModel.experiment_id == experiment_id)
                .order_by(GenerationModel.generation_number)
                .all()
            )
            return [
                Generation(
                    id=r.id,
                    number=r.generation_number,
                    experiment_id=r.experiment_id,
                    best_fitness=r.best_fitness
                )
                for r in rows
            ]
        finally:
            session.close()