from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.sql import func
from config.database import Base
import uuid

class Farmer(Base):
    __tablename__ = "farmers"
    
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    land_size = Column(Float, nullable=False)  # in acres
    crop_type = Column(String(50), nullable=False)
    irrigation = Column(String(50), nullable=False)  # drip, flood, sprinkler
    tillage = Column(String(50), nullable=False)  # conventional, no-till, reduced
    location = Column(Text, nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Farmer(farmer_id='{self.farmer_id}', name='{self.name}')>"

class CarbonCredit(Base):
    __tablename__ = "carbon_credits"
    
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(String(20), nullable=False, index=True)
    credit_id = Column(String(30), unique=True, index=True, nullable=False)
    carbon_sequestered = Column(Float, nullable=False)  # in tons CO2
    verification_status = Column(String(20), default="pending")  # pending, verified, rejected
    calculation_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<CarbonCredit(credit_id='{self.credit_id}', carbon_sequestered={self.carbon_sequestered})>"

class FarmActivity(Base):
    __tablename__ = "farm_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(String(20), nullable=False, index=True)
    activity_type = Column(String(50), nullable=False)  # planting, harvesting, irrigation
    activity_date = Column(DateTime(timezone=True), nullable=False)
    description = Column(Text, nullable=True)
    carbon_impact = Column(Float, nullable=True)  # in kg CO2
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<FarmActivity(farmer_id='{self.farmer_id}', activity_type='{self.activity_type}')>"
