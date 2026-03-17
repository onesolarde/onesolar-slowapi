
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User, SolarPark, MaintenanceRecord

router = APIRouter(prefix="/solar-parks", tags=["solar-parks"])

def load_all_solar_parks(db: Session) -> list[SolarPark]:
    return [*db.execute(select(SolarPark)).scalars().all()]


@router.get("/")
def get_all_solar_parks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    solar_parks = db.execute(select(SolarPark)).scalars().all()
    return solar_parks


@router.get("/{solar_park_id}/maintenance-records")
def get_maintenance_records_by_solar_park_route(
    solar_park_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[MaintenanceRecord]:
    from .maintenance import load_maintenance_records

    records = load_maintenance_records(db)
    records_for_park = [record for record in records if record.solar_park_id == solar_park_id]
    
    return records_for_park