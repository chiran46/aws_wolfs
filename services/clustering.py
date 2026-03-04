import uuid
import boto3
from decimal import Decimal
from config.aws_config import farmers_table, clusters_table

class ClusteringService:
    
    @staticmethod
    def generate_cluster_id() -> str:
        """Generate unique cluster ID"""
        return f"CLS_{uuid.uuid4().hex[:8].upper()}"
    
    @staticmethod
    def create_cluster(cluster_name: str, cluster_type: str = "default") -> str:
        """Create a new cluster"""
        cluster_id = ClusteringService.generate_cluster_id()
        
        clusters_table.put_item(
            Item={
                "cluster_id": cluster_id,
                "cluster_name": cluster_name,
                "cluster_type": cluster_type,
                "farmer_count": Decimal("0"),
                "total_carbon": Decimal("0"),
                "farmers": [],
                "created_at": "2024-01-01T00:00:00Z",  # Dummy timestamp
                "status": "active"
            }
        )
        
        return cluster_id
    
    @staticmethod
    def assign_farmer_to_region_cluster(farmer: dict, carbon_amount: float) -> str:
        """Assign farmer to region-based cluster (one region = one cluster)"""
        location = farmer.get("location", "unknown").lower()
        
        # Simple region extraction (you can make this more sophisticated)
        if "california" in location:
            region_name = "California"
        elif "texas" in location:
            region_name = "Texas"
        elif "india" in location:
            region_name = "India"
        else:
            region_name = "Other"
        
        cluster_name = f"{region_name}_Region_Cluster"
        
        # Try to find existing cluster for this region
        try:
            # For simplicity, we'll scan for existing clusters
            # In production, you might want a more efficient approach
            response = clusters_table.scan(
                FilterExpression=boto3.dynamodb.conditions.Attr("cluster_name").eq(cluster_name)
            )
            
            if response["Items"]:
                # Cluster exists, update it
                cluster = response["Items"][0]
                cluster_id = cluster["cluster_id"]
                
                # Update cluster with new farmer and carbon
                current_farmers = cluster.get("farmers", [])
                current_carbon = float(cluster.get("total_carbon", 0))
                
                if farmer["farmer_id"] not in current_farmers:
                    current_farmers.append(farmer["farmer_id"])
                    new_carbon = current_carbon + carbon_amount
                    
                    clusters_table.update_item(
                        Key={"cluster_id": cluster_id},
                        UpdateExpression="SET farmers = :farmers, total_carbon = :carbon, farmer_count = :count",
                        ExpressionAttributeValues={
                            ":farmers": current_farmers,
                            ":carbon": Decimal(str(new_carbon)),
                            ":count": Decimal(str(len(current_farmers)))
                        }
                    )
                
                return cluster_id
            else:
                # Create new cluster
                cluster_id = ClusteringService.create_cluster(cluster_name, "region_based")
                
                # Add farmer to new cluster
                clusters_table.update_item(
                    Key={"cluster_id": cluster_id},
                    UpdateExpression="SET farmers = :farmers, total_carbon = :carbon, farmer_count = :count",
                    ExpressionAttributeValues={
                        ":farmers": [farmer["farmer_id"]],
                        ":carbon": Decimal(str(carbon_amount)),
                        ":count": Decimal("1")
                    }
                )
                
                return cluster_id
                
        except Exception as e:
            # If anything fails, create a new cluster
            cluster_id = ClusteringService.create_cluster(cluster_name, "region_based")
            clusters_table.update_item(
                Key={"cluster_id": cluster_id},
                UpdateExpression="SET farmers = :farmers, total_carbon = :carbon, farmer_count = :count",
                ExpressionAttributeValues={
                    ":farmers": [farmer["farmer_id"]],
                    ":carbon": Decimal(str(carbon_amount)),
                    ":count": Decimal("1")
                }
            )
            return cluster_id
    
    @staticmethod
    def get_cluster_info(cluster_id: str) -> dict:
        """Get cluster information"""
        response = clusters_table.get_item(Key={"cluster_id": cluster_id})
        
        if "Item" not in response:
            raise Exception(f"Cluster {cluster_id} not found")
        
        return response["Item"]
