from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.farmer import Farmer, CarbonCredit, FarmActivity
from typing import List, Optional
import uuid
from datetime import datetime

class FarmerService:
    
    @staticmethod
    def generate_farmer_id() -> str:
        """Generate unique farmer ID"""
        return f"FRM_{uuid.uuid4().hex[:8].upper()}"
    
    @staticmethod
    def create_farmer(db: Session, farmer_data: dict) -> Farmer:
        """Create a new farmer in the database"""
        farmer_id = FarmerService.generate_farmer_id()
        
        db_farmer = Farmer(
            farmer_id=farmer_id,
            name=farmer_data["name"],
            land_size=farmer_data["land_size"],
            crop_type=farmer_data["crop_type"],
            irrigation=farmer_data["irrigation"],
            tillage=farmer_data["tillage"],
            location=farmer_data["location"],
            phone=farmer_data.get("phone"),
            email=farmer_data.get("email")
        )
        
        db.add(db_farmer)
        db.commit()
        db.refresh(db_farmer)
        return db_farmer
    
    @staticmethod
    def get_farmer_by_id(db: Session, farmer_id: str) -> Optional[Farmer]:
        """Get farmer by farmer_id"""
        return db.query(Farmer).filter(Farmer.farmer_id == farmer_id).first()
    
    @staticmethod
    def get_all_farmers(db: Session, skip: int = 0, limit: int = 100) -> List[Farmer]:
        """Get all farmers with pagination"""
        return db.query(Farmer).filter(Farmer.is_active == True).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_farmer(db: Session, farmer_id: str, farmer_data: dict) -> Optional[Farmer]:
        """Update farmer information"""
        db_farmer = FarmerService.get_farmer_by_id(db, farmer_id)
        if not db_farmer:
            return None
        
        for key, value in farmer_data.items():
            if hasattr(db_farmer, key) and value is not None:
                setattr(db_farmer, key, value)
        
        db.commit()
        db.refresh(db_farmer)
        return db_farmer
    
    @staticmethod
    def delete_farmer(db: Session, farmer_id: str) -> bool:
        """Soft delete farmer (set is_active to False)"""
        db_farmer = FarmerService.get_farmer_by_id(db, farmer_id)
        if not db_farmer:
            return False
        
        db_farmer.is_active = False
        db.commit()
        return True
    
    @staticmethod
    def get_farmers_by_location(db: Session, location: str) -> List[Farmer]:
        """Get farmers by location"""
        return db.query(Farmer).filter(
            and_(Farmer.location.ilike(f"%{location}%"), Farmer.is_active == True)
        ).all()
    
    @staticmethod
    def get_farmers_by_crop_type(db: Session, crop_type: str) -> List[Farmer]:
        """Get farmers by crop type"""
        return db.query(Farmer).filter(
            and_(Farmer.crop_type == crop_type, Farmer.is_active == True)
        ).all()

class CarbonCreditService:
    
    @staticmethod
    def generate_credit_id() -> str:
        """Generate unique carbon credit ID"""
        return f"CRD_{uuid.uuid4().hex[:10].upper()}"
    
    @staticmethod
    def create_carbon_credit(db: Session, farmer_id: str, carbon_data: dict) -> CarbonCredit:
        """Create carbon credit for a farmer"""
        credit_id = CarbonCreditService.generate_credit_id()
        
        db_credit = CarbonCredit(
            farmer_id=farmer_id,
            credit_id=credit_id,
            carbon_sequestered=carbon_data["carbon_sequestered"],
            verification_status="pending"
        )
        
        db.add(db_credit)
        db.commit()
        db.refresh(db_credit)
        return db_credit
    
    @staticmethod
    def get_credits_by_farmer(db: Session, farmer_id: str) -> List[CarbonCredit]:
        """Get all carbon credits for a farmer"""
        return db.query(CarbonCredit).filter(CarbonCredit.farmer_id == farmer_id).all()

class FarmActivityService:
    
    @staticmethod
    def create_activity(db: Session, farmer_id: str, activity_data: dict) -> FarmActivity:
        """Create farm activity record"""
        db_activity = FarmActivity(
            farmer_id=farmer_id,
            activity_type=activity_data["activity_type"],
            activity_date=activity_data["activity_date"],
            description=activity_data.get("description"),
            carbon_impact=activity_data.get("carbon_impact")
        )
        
        db.add(db_activity)
        db.commit()
        db.refresh(db_activity)
        return db_activity
    
    @staticmethod
    def get_activities_by_farmer(db: Session, farmer_id: str) -> List[FarmActivity]:
        """Get all activities for a farmer"""
        return db.query(FarmActivity).filter(FarmActivity.farmer_id == farmer_id).all()
