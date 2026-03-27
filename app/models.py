
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = mapped_column(Integer, primary_key=True, index=True)
    username = mapped_column(String, unique=True, index=True, nullable=False)
    email = mapped_column(String, unique=True, index=True, nullable=False)
    password = mapped_column(String, nullable=False)


class SolarPark(Base):
    __tablename__ = "solar_parks"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, unique=True, index=True, nullable=False)
    location = mapped_column(String, nullable=False)
    energy_output = mapped_column(Integer, nullable=False)


class Inverter(Base):
    __tablename__ = "inverters"

    id = mapped_column(Integer, primary_key=True, index=True)
    solar_park_id = mapped_column(Integer, nullable=False)
    software_version = mapped_column(String, nullable=False)


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id = mapped_column(Integer, primary_key=True, index=True)
    solar_park_id = mapped_column(Integer, nullable=False)
    description = mapped_column(String, nullable=False)
    date = mapped_column(String, nullable=False)