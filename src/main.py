from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from interfaces.api.routes import router
from infrastructure.database.connection import engine
from infrastructure.database.models import Base

app = FastAPI(title="FERMEST API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(router)