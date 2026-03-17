
from pydantic import BaseModel

# Users

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserUpdate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str


# Auth

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# Solar Parks

class SolarParkCreate(BaseModel):
    name: str
    location: str
    energy_output: int

class SolarParkUpdate(BaseModel):
    name: str
    location: str
    energy_output: int

class SolarParkResponse(BaseModel):
    id: int
    name: str
    location: str
    energy_output: int

# Maintenance Records

class MaintenanceRecordCreate(BaseModel):
    solar_park_id: int
    description: str
    date: str

class MaintenanceRecordUpdate(BaseModel):
    solar_park_id: int
    description: str
    date: str

class MaintenanceRecordResponse(BaseModel):
    id: int
    solar_park_id: int
    description: str
    date: str
