import unittest
from unittest.mock import patch, mock_open
import json
from src.services.order import Order


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.mock_products = [
            {"Email": "test@example.com", "OrderNumber": "1001", "Status": "Shipped"},
            {"Email": "test@example.com", "OrderNumber": "1002", "Status": "Processing"},
            {"Email": "other@example.com", "OrderNumber": "1003", "Status": "Delivered"}
        ]
        
    @patch('builtins.open', new_callable=mock_open)
    def test_init(self, mock_file):
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(self.mock_products)
        
        order = Order()
        self.assertEqual(len(order.product_data), 3)
    
    @patch('builtins.open', new_callable=mock_open)
    def test_order_status(self, mock_file):
        
        with patch.object(Order, '__init__', lambda self: None):
            order = Order()
            order.product_data = self.mock_products
            order.orders = {
                "1001": self.mock_products[0],
                "1002": self.mock_products[1],
                "1003": self.mock_products[2]
            }
            
            self.assertEqual(order.order_status("1001"), self.mock_products[0])
            
            not_found_msg = "Could not find an order with order number: 9999."
            self.assertEqual(order.order_status("9999"), not_found_msg)
    
    @patch('builtins.open', new_callable=mock_open)
    def test_order_numbers(self, mock_file):
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(self.mock_products)
        
        with patch.object(Order, '__init__', lambda self: None):
            order = Order()
            order.order_nums_by_email = {
                "test@example.com": ["1001", "1002"],
                "other@example.com": ["1003"]
            }
            
            self.assertEqual(order.order_numbers("test@example.com"), ["1001", "1002"])
            self.assertEqual(order.order_numbers("nonexistent@example.com"), [])


if __name__ == '__main__':
    unittest.main()
