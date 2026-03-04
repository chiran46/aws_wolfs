from member3_cluster import CarbonClusterAggregator
from member3_market import MarketSimulator
from member3_engine import CarbonEstimationEngine

engine = CarbonEstimationEngine()
cluster_aggregator = CarbonClusterAggregator()
market_sim = MarketSimulator()

farmers = [
    engine.estimate_credits(5, "cover_crop", "clay", "images/yield1.jpg"),
    engine.estimate_credits(3, "cover_crop", "sandy", "images/yield2.jpg"),
]

pool = cluster_aggregator.create_cluster(farmers, "Karnataka", "cover_crop")
market_ready = market_sim.market_ready_score(pool)
print("------ MARKET OUTPUT ------")
print(market_ready)