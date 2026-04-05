from fastapi import FastAPI
from interfaces.api.routes import router
from infrastructure.database.connection import engine
from infrastructure.database.models import Base

app = FastAPI(title="FERMEST API")

Base.metadata.create_all(bind=engine)

app.include_router(router)