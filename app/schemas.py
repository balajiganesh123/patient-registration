from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing import Literal

class PatientCreate(BaseModel):
    mrn : str = Field(pattern=r"^[0-9]{8}$")
    first_name : str = Field(min_length=1, max_length=100)
    last_name : str = Field(min_length=1, max_length=100)
    date_of_birth : date = Field()
    sex : Literal["male", "female", "others", "unknown"]
    phone : str | None = Field(default=None, pattern=r"^[0-9]{10}$")
    address_line1 : str = Field(min_length=1, max_length=200)
    address_line2 : str | None = None
    city : str = Field(min_length=1, max_length=100)
    state : str = Field(pattern=r"^[A-Z]{2}$")
    zip_code : str = Field(pattern=r"^[0-9]{5}$")
    insurance_member_id : str | None = None
    emergency_contact_name : str | None = None
    emergency_contact_phone : str | None = Field(default=None, pattern=r"^[0-9]{10}$")
    
    @field_validator("date_of_birth", mode="after")
    @classmethod
    def validate_dob(cls, value: date) -> date:
        if value >= date.today():
            raise ValueError("date of birth must be in past")
        
        return value
    
    @model_validator(mode="after")
    def validate_(self) -> "PatientCreate":
        phone = self.emergency_contact_phone
        name = self.emergency_contact_name
        
        if phone is not None and (name is None or name.strip() == ""):
            raise ValueError("emergency_contact_name is required when emergency_contact_phone is provided")
            
        return self

class PatientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    mrn : str
    first_name : str
    last_name : str
    date_of_birth : date
    sex : str
    phone : str | None
    address_line1 : str
    address_line2 : str | None
    city : str
    state : str
    zip_code : str
    insurance_member_id : str | None
    emergency_contact_name : str | None
    emergency_contact_phone : str | None
    created_at : datetime
    
class PatientSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    mrn : str
    first_name : str
    last_name : str
    date_of_birth : date
    sex : str
    created_at : datetime