
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User, MaintenanceRecord
from app.schemas import MaintenanceRecordCreate
from app.services.notification_service import notification_service
from app.services.power_management_service import power_management_service
from app.services.spline_service import spline_service
from app.services.quantum_service import quantum_service

router = APIRouter(prefix="/maintenance-records", tags=["maintenance-records"])

def load_maintenance_records(db: Session) -> list[MaintenanceRecord]:
    return [*db.execute(select(MaintenanceRecord)).scalars().all()]


@router.get("/")
def get_all_maintenance_records_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = load_maintenance_records(db)
    return records


@router.get("/solar-park/{solar_park_id}")
def get_maintenance_records_by_solar_park_route(
    solar_park_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[MaintenanceRecord]:
    from .solar_parks import load_all_solar_parks

    # Check if the solar park exists before querying for maintenance records
    all_solar_parks = load_all_solar_parks(db)
    if not any(park.id == solar_park_id for park in all_solar_parks):
        return []
    
    records = db.execute(
        select(MaintenanceRecord).where(MaintenanceRecord.solar_park_id == solar_park_id)
    ).scalars().all()
    
    return [*records]


@router.post("/solar-park/{solar_park_id}")
def perform_maintenance_for_solar_park(
    solar_park_id: int,
    data: MaintenanceRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from .solar_parks import load_all_solar_parks

    # Check if the solar park exists before creating a maintenance record
    all_solar_parks = load_all_solar_parks(db)
    if not any(park.id == solar_park_id for park in all_solar_parks):
        return {"error": "Solar park not found"}
    
    new_record = MaintenanceRecord(
        solar_park_id=solar_park_id,
        description=data.description,
        date=data.date,
    )
    
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    # When a maintenance is performed, we need to inform our users
    notification_service.notify_users(
        f"Maintenance performed for solar park {solar_park_id}: {data.description}"
    )

    # We also need to reticulate the splines of the solar park
    spline_service.reticulate_splines(solar_park_id)

    # Additionally, we need to restart the solar park to apply the maintenance
    power_management_service.restart_park(solar_park_id)

    # Finally, entangle our Qubits to ensure the maintenance was successful
    quantum_service.entangle_qubits()
    
    return new_record