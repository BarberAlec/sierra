import json


PRODUCT_PATH = "src/data/products.json"


class Product:
    """
    A singleton class to manage and query product data.
    
    The `Product` class reads product data from a JSON file and provides methods
    to show availablity and descriptions.
    """
    _instance = None

    SKU_KEY = "SKU"
    NAME_KEY = "ProductName"
    INVENTORY_KEY = "Inventory"
    DESCRIPTION_KEY = "Description"
    TAGS_KEY = "Tags"
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        with open(PRODUCT_PATH, "r") as f:
            self.product_data = json.load(f)
        
        self.products = {}
        for product in self.product_data:
            self.products[product[self.SKU_KEY]] = product
    
    def availablity(self, skus: list[str]) -> str:
        found = lambda sku, units: f"{units} units available for sku {sku}"
        not_found = lambda sku: f"Could not find product with sku {sku}"
        
        res = []
        for sku in skus:
            a = self.products.get(sku, None)
            if a is None:
                res.append(not_found(sku))
            else:
                units = a[self.INVENTORY_KEY]
                res.append(found(sku, units))
        concat_result = "\n".join(res)
        return concat_result
    
    def product_details(self, sku):
        if sku not in self.products:
            return f"Could not find product with SKU {sku}"
        
        prdct = self.products[sku]
        return f"{prdct[self.NAME_KEY]} (SKU: {prdct[self.SKU_KEY]})\n{prdct[self.DESCRIPTION_KEY]}\nTags: {prdct[self.TAGS_KEY]}"
    
    def product_descriptions(self) -> str:
        # for now this will return them all as scope is small
        # TODO: create Product model and use __str__ to generate user visible data
        # we could do more precise search using tags? for now let LLM descide from provided descriptions
        res = []
        for prd in self.product_data:
            sku, name, desc = prd[self.SKU_KEY], prd[self.NAME_KEY], prd[self.DESCRIPTION_KEY]
            desc_with_sku = f"SKU: {sku} -> {name}: {desc}"
            res.append(desc_with_sku)
        concat_result = "\n".join(res)
        return concat_result
        
