# Mock DynamoDB implementation for testing
class MockTable:
    def __init__(self, table_name):
        self.table_name = table_name
        self.items = []
    
    def put_item(self, Item):
        self.items.append(Item)
        print(f"Mock: Added item to {self.table_name}: {Item}")
    
    def get_item(self, Key):
        for item in self.items:
            if item.get('farmer_id') == Key.get('farmer_id'):
                return {'Item': item}
        return {}
    
    def scan(self):
        return {'Items': self.items}

class MockDynamoDB:
    def Table(self, table_name):
        return MockTable(table_name)

# Create mock instance
mock_dynamodb = MockDynamoDB()
farmers_table = mock_dynamodb.Table("Farmers")
