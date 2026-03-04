from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
from decimal import Decimal
from config.aws_config import farmers_table, clusters_table
from services.clustering import ClusteringService

router = APIRouter()

class Farmer(BaseModel):
    name: str
    land_size: float
    crop_type: str
    irrigation: str
    tillage: str
    location: str

class FarmerAssessment(BaseModel):
    eligible: bool
    estimated_carbon: float  # in tons CO2
    income_projection: float  # in USD
    cluster_id: Optional[str] = None
    cluster_name: Optional[str] = None

class ClusterAssignment(BaseModel):
    farmer_id: str
    cluster_id: str
    cluster_name: str
    message: str

@router.post("/farmer/register")
def register_farmer(farmer: Farmer):
    farmer_id = str(uuid.uuid4())

    farmers_table.put_item(
        Item={
            "farmer_id": farmer_id,
            "name": farmer.name,
            "land_size": Decimal(str(farmer.land_size)),
            "crop_type": farmer.crop_type,
            "irrigation": farmer.irrigation,
            "tillage": farmer.tillage,
            "location": farmer.location,
        }
    )

    return {
        "message": "Farmer registered successfully",
        "farmer_id": farmer_id
    }

@router.post("/farmer/assessment/{farmer_id}", response_model=FarmerAssessment)
def assess_farmer(farmer_id: str):
    try:
        # Fetch farmer from DynamoDB
        response = farmers_table.get_item(Key={"farmer_id": farmer_id})
        
        if "Item" not in response:
            raise HTTPException(status_code=404, detail="Farmer not found")
        
        farmer = response["Item"]
        
        # Dummy carbon calculation (for now)
        # This will be replaced by Sachin's carbon logic
        estimated_carbon = 4.2  # Dummy value
        income_projection = 240.0  # Dummy value
        
        # Assign farmer to cluster
        cluster_id = ClusteringService.assign_farmer_to_region_cluster(farmer, estimated_carbon)
        cluster_info = ClusteringService.get_cluster_info(cluster_id)
        
        # Return assessment with cluster info
        assessment = FarmerAssessment(
            eligible=True,
            estimated_carbon=estimated_carbon,
            income_projection=income_projection,
            cluster_id=cluster_id,
            cluster_name=cluster_info.get("cluster_name", "Unknown")
        )
        
        return assessment
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Assessment failed: {str(e)}")

@router.post("/farmer/cluster/{farmer_id}", response_model=ClusterAssignment)
def assign_farmer_to_cluster(farmer_id: str):
    try:
        # Fetch farmer from DynamoDB
        response = farmers_table.get_item(Key={"farmer_id": farmer_id})
        
        if "Item" not in response:
            raise HTTPException(status_code=404, detail="Farmer not found")
        
        farmer = response["Item"]
        
        # Assign to cluster using clustering logic
        cluster_id = ClusteringService.simple_clustering_logic(farmer)
        
        # Get cluster info
        cluster_info = ClusteringService.get_cluster_info(cluster_id)
        
        return ClusterAssignment(
            farmer_id=farmer_id,
            cluster_id=cluster_id,
            cluster_name=cluster_info.get("cluster_name", "Unknown"),
            message=f"Farmer assigned to cluster {cluster_id}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clustering failed: {str(e)}")
