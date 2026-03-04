class MarketSimulator:
    def __init__(self):
        self.esg_factor = 1.05  # Dummy factor for ESG score

    def market_ready_score(self, cluster_data):
        cluster_data['market_ready'] = True
        cluster_data['esg_score'] = round(cluster_data['quality_score'] * self.esg_factor, 2)
        return cluster_data