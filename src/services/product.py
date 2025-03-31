import json
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

        product_units_status = []
        for sku in skus:
            a = self.products.get(sku, None)
            if a is None:
                self.logger.warning(f"Product not found: {sku}")
                product_units_status.append(not_found(sku))
            else:
                units = a[self.INVENTORY_KEY]
                self.logger.info(f"Found product {sku} with {units} units available")
                product_units_status.append(found(sku, units))

        return "\n".join(product_units_status)

    def product_details(self, sku):
        self.logger.info(f"Getting details for product: {sku}")
        if sku not in self.products:
            self.logger.warning(f"Product not found: {sku}")
            return f"Could not find product with SKU {sku}"

        prd = self.products[sku]
        name, description, tags = map(prd.get, (self.NAME_KEY, self.DESCRIPTION_KEY, self.TAGS_KEY))
        self.logger.info(f"Found product details for {sku}: {name}")

        return f"{name} (SKU: {sku})\n{description}\nTags: {tags}"

    def product_descriptions(self) -> str:        
        # for now this will return them all products. There are only a few so this is fine
        # consider using QDrant or other VectorDB if size is larger
        # TODO: create Product model and use __str__ to generate user visible data
        self.logger.info("Retrieving all product descriptions")
        product_descriptions = []
        for prd in self.product_data:
            sku, name, desc = map(prd.get, (self.SKU_KEY, self.NAME_KEY, self.DESCRIPTION_KEY))
            desc_with_sku = f"SKU: {sku} -> {name}: {desc}"
            product_descriptions.append(desc_with_sku)

        self.logger.info(f"Retrieved descriptions for {len(self.product_data)} products")
        return "\n".join(product_descriptions)
