from app.models.item import Item
from app.models.receipt import Receipt
from app.serializers.receipt_model import ReceiptModel
from app.serializers.item_model import ItemModel
from typing import List
import math
from datetime import datetime
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Backend:
    def __init__(self):
        self.database = {}
        self.cache = {}
    
    def add_receipt(self, receipt_request):
        try:
            
            items = self.create_items(receipt_request.items)
            
            receipt = Receipt(
                retailer=receipt_request.retailer,
                purchaseDate=receipt_request.purchaseDate,
                purchaseTime=receipt_request.purchaseTime,
                total=receipt_request.total,
                items=items
            )
            self.database[receipt.id] = receipt
            
            return { "success": True, "id": receipt.id }
        except ValueError as e:
            return { "success": False, "error": str(e) }
        except Exception as e:
            return { "success": False, "error": str(e) }

    def create_items(self, items: List[ItemModel]):
        result = []
        for each in items:
            result.append(Item(shortDescription=each.shortDescription, price=each.price))
        return result

    def get_points(self, receipt_id):
        try:
            points = self.__calculate_points(receipt_id)
            return { "points": points}
        except KeyError:
            return None
        except Exception as e:
            return { "error": str(e) }


    def __calculate_points(self, receipt_id):
        # caching
        if receipt_id in self.cache:
            return self.cache[receipt_id]
        
        # database
        receipt = self.database[receipt_id]
        points = 0
        points += self.__retailer(receipt.retailer)
        points += self.__total(receipt.total)
        points += self.__items(receipt.items)
        points += self.__purchase_date(receipt.purchaseDate)    
        points += self.__purchase_time(receipt.purchaseTime)
        
        self.cache[receipt_id] = points
        return points

    def __retailer(self, retailer):
        point = 0
        for c in retailer:
            # One point for every alphanumeric character in the retailer name.
            if c.isalnum():
                point += 1
        return point

    def __total(self, total):
        point = 0
        if float(total).is_integer():
            # 50 points if the total is a round dollar amount with no cents.
            point += 50
        if float(total) % 0.25 == 0:
            # 25 points if the total is a multiple of `0.25`
            point += 25
        return point

    def __items(self, items):
        point = 0
        # 5 points for every two items on the receipt
        point += (len(items) // 2) * 5
        for item in items:
            if len(item.shortDescription.strip()) % 3 == 0:
                point += math.ceil(0.2 * float(item.price))
        return point
    
    def __purchase_date(self, purchaseDate):
        point = 0
        date = datetime.strptime(purchaseDate, "%Y-%m-%d")
        # 6 points if the day in the purchase date is odd.
        if date.day % 2 == 1:
            point += 6
        return point
    
    def __purchase_time(self, purchaseTime):
        point = 0
        time = datetime.strptime(purchaseTime, "%H:%M").time()
        # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
        if 14 <= time.hour <= 15:
            if time.hour == 14 and time.minute == 0:
                return point
            else:
                point += 10
                return point
        return point
    
            



        