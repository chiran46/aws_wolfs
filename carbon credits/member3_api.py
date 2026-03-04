from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from member3_engine import CarbonEstimationEngine
from member3_cluster import CarbonClusterAggregator
from member3_market import MarketSimulator

router = APIRouter()
engine = CarbonEstimationEngine()
cluster_aggregator = CarbonClusterAggregator()
market_sim = MarketSimulator()

class EstimateRequest(BaseModel):
    land_area: float
    practice_type: str
    soil_type: str = None
    yield_image: str = None

@router.post("/member3/estimate")
def estimate_carbon(data: EstimateRequest):
    try:
        credit = engine.estimate_credits(
            land_area=data.land_area,
            practice_type=data.practice_type,
            soil_type=data.soil_type,
            yield_image=data.yield_image
        )
        return credit
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))