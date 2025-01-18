from typing import List
import uuid
from app.models.item import Item

class Receipt:
    def __init__(self, retailer: str, purchaseDate: str, purchaseTime: str, items: List[Item], total: str):
        self.id = uuid.uuid4()
        self.retailer = retailer
        self.purchaseDate = purchaseDate
        self.purchaseTime = purchaseTime
        self.items = items
        self.total = total
        





