from fastapi import FastAPI
from app.routers.patients import router as patients_router

app = FastAPI(title="Patient Registration API", version="0.1.0")

app.include_router(patients_router)