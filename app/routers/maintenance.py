
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User, MaintenanceRecord
from app.schemas import MaintenanceRecordCreate
from app.services.notification_service import notification_service
from app.services.grid_connection_service import grid_connection_service

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

    # Disconnect the solar park from the grid before performing maintenance
    grid_connection_service.disconnect_park_from_grid(solar_park_id)

    # Update inverters if software version is outdated
    updated_inverters = grid_connection_service.update_inverters()

    # Additionally, we need to restart the solar park to apply the maintenance
    grid_connection_service.reconnect_park_to_grid(solar_park_id)

    # Generate maintenance report
    grid_connection_service.write_report(solar_park_id, updated_inverters)
    
    # After a maintenance is performed, we need to inform our users
    notification_service.notify_users(
        f"Maintenance performed for solar park {solar_park_id}: {data.description}"
    )

    return new_record