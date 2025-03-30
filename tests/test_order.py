import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
from src.services.order import Order
from src.services.product import Product


class TestOrder(unittest.TestCase):
    def setUp(self):
        Order._reset()
        Product._reset()
        
        self.mock_products = [
            {"Email": "test@example.com", "OrderNumber": "1001", "Status": "Shipped", "ProductsOrdered": [], "CustomerName": "Bob", "TrackingNumber": "1234"},
            {"Email": "test@example.com", "OrderNumber": "1002", "Status": "Processing", "ProductsOrdered": [], "CustomerName": "Mary", "TrackingNumber": "5555"},
            {"Email": "other@example.com", "OrderNumber": "1003", "Status": "Delivered", "ProductsOrdered": [], "CustomerName": "Sean", "TrackingNumber": "7777"}
        ]

    @patch('src.services.order.open', new_callable=mock_open)
    @patch('src.services.product.open', new_callable=mock_open)
    def test_init(self, mock_order_file, mock_product_file):
        mock_order_file.return_value.__enter__.return_value.read.return_value = json.dumps([])
        mock_product_file.return_value.__enter__.return_value.read.return_value = json.dumps(self.mock_products)

        order = Order()
        self.assertEqual(len(order.product_data), 3)
    
    def test_order_status(self):
        
        with patch.object(Order, '__init__', lambda self: None):
            order = Order()
            order.product_data = self.mock_products
            order.logger = MagicMock()
            order.orders = {
                "#1001": self.mock_products[0],
                "#1002": self.mock_products[1],
                "#1003": self.mock_products[2]
            }
            
            res = "Order #1001 for Bob (test@example.com)\nStatus: Shipped\nTracking number: 1234\n"
            self.assertEqual(order.order_status("1001"), res)
            
            not_found_msg = "Could not find an order with order number: #9999."
            self.assertEqual(order.order_status("9999"), not_found_msg)
    
    @patch('src.services.order.open', new_callable=mock_open)
    @patch('src.services.product.open', new_callable=mock_open)
    def test_order_numbers(self, mock_order_file, mock_product_file):
        mock_order_file.return_value.__enter__.return_value.read.return_value = json.dumps([])
        mock_product_file.return_value.__enter__.return_value.read.return_value = json.dumps(self.mock_products)
        
        with patch.object(Order, '__init__', lambda self: None):
            order = Order()
            order.logger = MagicMock()
            order.order_nums_by_email = {
                "test@example.com": ["1001", "1002"],
                "other@example.com": ["1003"]
            }
            
            self.assertEqual(order.order_numbers("test@example.com"), ["1001", "1002"])
            self.assertEqual(order.order_numbers("nonexistent@example.com"), [])


if __name__ == '__main__':
    unittest.main()
