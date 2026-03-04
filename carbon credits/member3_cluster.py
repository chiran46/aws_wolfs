from collections import defaultdict

class CarbonClusterAggregator:
    def __init__(self):
        self.pools = {}

    def create_cluster(self, farmers_data, location, practice_type):
        """
        farmers_data: list of dicts with 'carbon_credits_after_buffer'
        """
        cluster_id = f"POOL-{len(self.pools)+1:08X}"
        total_credits = sum(f['carbon_credits_after_buffer'] for f in farmers_data)
        total_farmers = len(farmers_data)
        quality_score = sum(f['carbon_credits_after_buffer']*1.03 for f in farmers_data)

        self.pools[cluster_id] = {
            'location': location,
            'practice_type': practice_type,
            'total_farmers': total_farmers,
            'total_credits': round(total_credits, 2),
            'status': 'Sellable',
            'pool_id': cluster_id,
            'quality_score': round(quality_score, 2)
        }
        return self.pools[cluster_id]