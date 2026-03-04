from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

from config.database import get_db
from services.farmer_service import FarmerService, CarbonCreditService, FarmActivityService
from models.farmer import Farmer, CarbonCredit, FarmActivity

router = APIRouter()

# Pydantic models for request/response
class FarmerRegistration(BaseModel):
    name: str
    land_size: float  # in acres
    crop_type: str
    irrigation: str  # e.g., "drip", "flood", "sprinkler"
    tillage: str  # e.g., "conventional", "no-till", "reduced"
    location: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class FarmerUpdate(BaseModel):
    name: Optional[str] = None
    land_size: Optional[float] = None
    crop_type: Optional[str] = None
    irrigation: Optional[str] = None
    tillage: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class FarmerResponse(BaseModel):
    farmer_id: str
    name: str
    land_size: float
    crop_type: str
    irrigation: str
    tillage: str
    location: str
    phone: Optional[str]
    email: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class CarbonCreditCreate(BaseModel):
    carbon_sequestered: float  # in tons CO2

class CarbonCreditResponse(BaseModel):
    credit_id: str
    farmer_id: str
    carbon_sequestered: float
    verification_status: str
    calculation_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class FarmActivityCreate(BaseModel):
    activity_type: str
    activity_date: datetime
    description: Optional[str] = None
    carbon_impact: Optional[float] = None  # in kg CO2

class FarmActivityResponse(BaseModel):
    id: int
    farmer_id: str
    activity_type: str
    activity_date: datetime
    description: Optional[str]
    carbon_impact: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True

# Farmer endpoints
@router.post("/farmer/register", response_model=FarmerResponse)
async def register_farmer(farmer: FarmerRegistration, db: Session = Depends(get_db)):
    try:
        db_farmer = FarmerService.create_farmer(db, farmer.dict())
        return db_farmer
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.get("/farmer/{farmer_id}", response_model=FarmerResponse)
async def get_farmer(farmer_id: str, db: Session = Depends(get_db)):
    db_farmer = FarmerService.get_farmer_by_id(db, farmer_id)
    if not db_farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return db_farmer

@router.get("/farmers", response_model=List[FarmerResponse])
async def get_all_farmers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    farmers = FarmerService.get_all_farmers(db, skip=skip, limit=limit)
    return farmers

@router.put("/farmer/{farmer_id}", response_model=FarmerResponse)
async def update_farmer(
    farmer_id: str, 
    farmer_update: FarmerUpdate, 
    db: Session = Depends(get_db)
):
    db_farmer = FarmerService.update_farmer(db, farmer_id, farmer_update.dict(exclude_unset=True))
    if not db_farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return db_farmer

@router.delete("/farmer/{farmer_id}")
async def delete_farmer(farmer_id: str, db: Session = Depends(get_db)):
    success = FarmerService.delete_farmer(db, farmer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return {"message": "Farmer deleted successfully"}

@router.get("/farmers/location/{location}", response_model=List[FarmerResponse])
async def get_farmers_by_location(location: str, db: Session = Depends(get_db)):
    farmers = FarmerService.get_farmers_by_location(db, location)
    return farmers

@router.get("/farmers/crop/{crop_type}", response_model=List[FarmerResponse])
async def get_farmers_by_crop_type(crop_type: str, db: Session = Depends(get_db)):
    farmers = FarmerService.get_farmers_by_crop_type(db, crop_type)
    return farmers

# Carbon Credit endpoints
@router.post("/farmer/{farmer_id}/carbon-credit", response_model=CarbonCreditResponse)
async def create_carbon_credit(
    farmer_id: str,
    carbon_data: CarbonCreditCreate,
    db: Session = Depends(get_db)
):
    # Verify farmer exists
    farmer = FarmerService.get_farmer_by_id(db, farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    try:
        db_credit = CarbonCreditService.create_carbon_credit(db, farmer_id, carbon_data.dict())
        return db_credit
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create carbon credit: {str(e)}")

@router.get("/farmer/{farmer_id}/carbon-credits", response_model=List[CarbonCreditResponse])
async def get_carbon_credits(farmer_id: str, db: Session = Depends(get_db)):
    # Verify farmer exists
    farmer = FarmerService.get_farmer_by_id(db, farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    credits = CarbonCreditService.get_credits_by_farmer(db, farmer_id)
    return credits

# Farm Activity endpoints
@router.post("/farmer/{farmer_id}/activity", response_model=FarmActivityResponse)
async def create_farm_activity(
    farmer_id: str,
    activity_data: FarmActivityCreate,
    db: Session = Depends(get_db)
):
    # Verify farmer exists
    farmer = FarmerService.get_farmer_by_id(db, farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    try:
        db_activity = FarmActivityService.create_activity(db, farmer_id, activity_data.dict())
        return db_activity
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create farm activity: {str(e)}")

@router.get("/farmer/{farmer_id}/activities", response_model=List[FarmActivityResponse])
async def get_farm_activities(farmer_id: str, db: Session = Depends(get_db)):
    # Verify farmer exists
    farmer = FarmerService.get_farmer_by_id(db, farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    activities = FarmActivityService.get_activities_by_farmer(db, farmer_id)
    return activities
