from member3_engine import CarbonEstimationEngine
from member3_cluster import CarbonClusterAggregator

engine = CarbonEstimationEngine()
cluster = CarbonClusterAggregator()

# Sample farmers
farmers = [
    engine.estimate_credits(5, "cover_crop", "clay", "images/yield1.jpg"),
    engine.estimate_credits(3, "cover_crop", "sandy", "images/yield2.jpg"),
    engine.estimate_credits(4, "cover_crop", "loamy", "images/yield3.jpg"),
]

pool = cluster.create_cluster(farmers, location="Karnataka", practice_type="cover_crop")
print("------ CLUSTER OUTPUT ------")
print(pool)