import json
import logging
from src.services.singleton import Singleton


PRODUCT_PATH = "src/data/products.json"


class Product(Singleton):
    """
    A singleton class to manage and query product data.
    
    The `Product` class reads product data from a JSON file and provides methods
    to show availablity and descriptions.
    """
    SKU_KEY = "SKU"
    NAME_KEY = "ProductName"
    INVENTORY_KEY = "Inventory"
    DESCRIPTION_KEY = "Description"
    TAGS_KEY = "Tags"
    
    def _initialize(self):
        with open(PRODUCT_PATH, "r") as f:
            self.product_data = json.load(f)
        
        self.products = {}
        for product in self.product_data:
            self.products[product[self.SKU_KEY]] = product
        self.logger.info(f"Loaded {len(self.product_data)} products")
    
    def availablity(self, skus: list[str]) -> str:
        self.logger.info(f"Checking availability for SKUs: {skus}")
        found = lambda sku, units: f"{units} units available for sku {sku}"
        not_found = lambda sku: f"Could not find product with sku {sku}"
        
        res = []
        for sku in skus:
            a = self.products.get(sku, None)
            if a is None:
                self.logger.warning(f"Product not found: {sku}")
                res.append(not_found(sku))
            else:
                units = a[self.INVENTORY_KEY]
                self.logger.info(f"Found product {sku} with {units} units available")
                res.append(found(sku, units))
        concat_result = "\n".join(res)
        return concat_result
    
    def product_details(self, sku):
        self.logger.info(f"Getting details for product: {sku}")
        if sku not in self.products:
            self.logger.warning(f"Product not found: {sku}")
            return f"Could not find product with SKU {sku}"
        
        prdct = self.products[sku]
        self.logger.info(f"Found product details for {sku}: {prdct[self.NAME_KEY]}")
        return f"{prdct[self.NAME_KEY]} (SKU: {prdct[self.SKU_KEY]})\n{prdct[self.DESCRIPTION_KEY]}\nTags: {prdct[self.TAGS_KEY]}"
    
    def product_descriptions(self) -> str:
        # for now this will return them all as scope is small
        # TODO: create Product model and use __str__ to generate user visible data
        # we could do more precise search using tags? for now let LLM descide from provided descriptions
        self.logger.info("Retrieving all product descriptions")
        res = []
        for prd in self.product_data:
            sku, name, desc = prd[self.SKU_KEY], prd[self.NAME_KEY], prd[self.DESCRIPTION_KEY]
            desc_with_sku = f"SKU: {sku} -> {name}: {desc}"
            res.append(desc_with_sku)
        concat_result = "\n".join(res)
        self.logger.info(f"Retrieved descriptions for {len(self.product_data)} products")
        return concat_result
        
