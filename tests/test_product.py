import unittest
from unittest.mock import patch, mock_open
import json
from src.services.product import Product


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.mock_products = [
            {"ProductName": "Bhavish's Backcountry Blaze Backpack", "SKU": "SOBP001", "Inventory": 120, "Description": "Conquer the wilderness!", "Tags": ["Backpack", "Hiking", "Adventure", "Outdoor Gear"]},
            {"ProductName": "Dorothy's Wizarding Red Shoes", "SKU": "SOSV009", "Inventory": 50, "Description": "Click your heels to teleport!", "Tags": ["Fashion", "Lifestyle", "Teleportation", "Transport"]},
            {"ProductName": "Nayely's Soarin' Surfboard", "SKU": "SOSV010", "Inventory": 7, "Description": "Ride the waves like never before!", "Tags": ["Water Sports", "Lifestyle", "Adventure", "Outdoors", "Transport"]}
        ]
        
    @patch('builtins.open', new_callable=mock_open)
    def test_init(self, mock_file):
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(self.mock_products)
        
        product = Product()
        self.assertEqual(len(product.product_data), 3)
    
    @patch('builtins.open', new_callable=mock_open)
    def test_availablity(self, mock_file):
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(self.mock_products)
        
        product = Product()
        
        self.assertEqual(product.availablity(["SOBP001", "SOSV009"]), "120 units available for sku SOBP001\n50 units available for sku SOSV009")
        self.assertEqual(product.availablity(["9999"]), "Could not find product with sku 9999")
    
    @patch('builtins.open', new_callable=mock_open)
    def test_product_descriptions(self, mock_file):
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(self.mock_products)
        
        product = Product()
        
        expected_res = [
            "SKU: SOBP001 -> Bhavish's Backcountry Blaze Backpack: Conquer the wilderness!",
            "SKU: SOSV009 -> Dorothy's Wizarding Red Shoes: Click your heels to teleport!",
            "SKU: SOSV010 -> Nayely's Soarin' Surfboard: Ride the waves like never before!"
        ]
        expected_res = "\n".join(expected_res)
            
        self.assertEqual(product.product_descriptions(), expected_res)


if __name__ == '__main__':
    unittest.main()
