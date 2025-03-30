import json
import logging
from collections import defaultdict
from src.services.product import Product


ORDER_PATH = "src/data/orders.json"


class Order:
    """
    A singleton class to manage and query order data.

    The `Order` class reads order data from a JSON file and provides methods
    to retrieve order statuses and order numbers by email.
    """
    _instance = None
    
    EMAIL_KEY = "Email"
    ORDER_NUM_KEY = "OrderNumber"
    PRODUCTS_LIST_KEY = "ProductsOrdered"
    TRACKING_KEY = "TrackingNumber"
    NAME_KEY = "CustomerName"
    STATUS_KEY = "Status"
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.product_helper = Product()
        self.logger = logging.getLogger(__name__)
        
        with open(ORDER_PATH, "r") as f:
            self.product_data = json.load(f)
        
        self.order_nums_by_email = defaultdict(list)
        self.orders = {}
        for order in self.product_data:
            self.order_nums_by_email[order[self.EMAIL_KEY]].append(order[self.ORDER_NUM_KEY])
            self.orders[order[self.ORDER_NUM_KEY]] = order
        self.logger.info(f"Loaded {len(self.product_data)} orders")
    
    def order_status(self, order_number: str):
        self.logger.info(f"Fetching status for order: {order_number}")
        order_number = f"#{order_number}" if order_number[0] != "#" else order_number
        if order_number not in self.orders:
            self.logger.warning(f"Order not found: {order_number}")
            return f"Could not find an order with order number: {order_number}."
        
        order = self.orders[order_number]
        product_details = [self._product_details(sku) for sku in order[self.PRODUCTS_LIST_KEY]]
        product_details = "\n".join(product_details)
        customer_name = order[self.NAME_KEY]
        customer_email = order[self.EMAIL_KEY]
        status = order[self.STATUS_KEY]
        tracking_number = order[self.TRACKING_KEY] or "N/A"
        
        self.logger.info(f"Retrieved order {order_number} with status: {status}")
        return f"Order {order_number} for {customer_name} ({customer_email})\nStatus: {status}\nTracking number: {tracking_number}\n{product_details}"
    
    def _product_details(self, sku) -> str:
        return self.product_helper.product_details(sku)
        
    def order_numbers(self, email: str):
        self.logger.info(f"Looking up order numbers for email: {email}")
        orders = self.order_nums_by_email.get(email, [])
        if not orders:
            self.logger.warning(f"No orders found for email: {email}")
        else:
            self.logger.info(f"Found {len(orders)} orders for email: {email}")
        return orders
