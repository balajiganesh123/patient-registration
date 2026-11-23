from datetime import datetime, UTC
from fastapi import APIRouter, HTTPException
from app.schemas import PatientCreate, PatientResponse, PatientSummary

patient_store : dict[str, PatientResponse] = {}

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/", status_code=201, response_model=PatientResponse)
async def register_patient(data : PatientCreate) -> PatientResponse:
    if data.mrn in patient_store:
        raise HTTPException(status_code=409, detail=f"Patient with MRN {data.mrn} is already registered")
    
    patient = PatientResponse(**data.model_dump(), created_at=datetime.now(UTC))
    
    patient_store[data.mrn] = patient
    
    return patient

@router.get("/{mrn}", response_model=PatientResponse)
async def get_patient(mrn : str) -> PatientResponse:
    if mrn not in patient_store:
        raise HTTPException(status_code=404, detail=f"Patient with MRN {mrn} not found")
    return patient_store[mrn]

@router.get("/", response_model=list[PatientSummary])
async def list_patients():
    return [PatientSummary.model_validate(patient, from_attributes=True) for patient in patient_store.values()]

