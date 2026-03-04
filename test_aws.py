import boto3
import os
from dotenv import load_dotenv

load_dotenv()

try:
    # Test AWS credentials
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    
    # Check if Farmers table exists
    try:
        farmers_table = dynamodb.Table("Farmers")
        farmers_table.load()
        print("✅ Farmers table exists and is accessible")
        
        # Test table description
        description = farmers_table.table_description
        print(f"Table status: {description.get('TableStatus', 'Unknown')}")
        print(f"Item count: {description.get('ItemCount', 0)}")
        
        # Test S3 bucket access
        s3 = boto3.resource(
            's3',
            region_name=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        
        bucket_name = os.getenv("S3_BUCKET_NAME")
        bucket = s3.Bucket(bucket_name)
        bucket.load()
        print(f"✅ S3 bucket '{bucket_name}' is accessible")
        
    except Exception as e:
        print(f"❌ Error accessing resources: {e}")

except Exception as e:
    print(f"❌ AWS connection failed: {e}")
    print("Please check your AWS credentials and region")
