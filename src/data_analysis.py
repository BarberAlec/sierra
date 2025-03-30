# unrealated file for investigating data, not part of main flow
import json


ORDERS_PATH = "src/data/orders.json"
PRODUCTS_PATH = "src/data/products.json"


def main():
    orders_data = products_data = None
    with open(ORDERS_PATH, "r") as f:
        orders_data = json.load(f)
        
    with open(PRODUCTS_PATH, "r") as f:
        products_data = json.load(f)
        
    statuses = set()
    for order in orders_data:
        statuses.add(order["Status"])
    print(statuses)
    # {'error', 'fulfilled', 'delivered', 'in-transit'}
    
    for order in orders_data:
        if order["TrackingNumber"] is not None:
            print(f"Status when tracking number: {order['Status']}")
    # 'delivered', 'in-transit' have Tracking number, others might, do we need to support/
    
    from collections import defaultdict
    counter = defaultdict(list)
    for order in orders_data:
        counter[order["Email"]].append(order["OrderNumber"])
    for k, v in counter.items():
        print(f"{k}: {v}\n")
    # one email for order number in data, cant rely on this...
    
    tags = set()
    for prd in products_data:
        [tags.add(t) for t in prd["Tags"]]
    print(tags)
    # {'Safety-Enhanced', 'Lifestyle', 'Explorer', 'Winter', 'High-Tech', 'Outdoor Gear', 'Backpack', 'Fashion', 'Weatherproof', 'Adventure-Ready', 'Adventure', 'Skis', 'Hiking', 'Comfort', 'Discretion', 'Advanced Cloaking', 'Versatile', 'Personal Flight', 'Teleportation', 'Snow', 'Stealth', 'Transport', 'Outdoors', 'Trail', 'Trailblazing', 'Rugged Design', 'Water Sports', 'Food & Beverage'}
    # likely not comprehensive, dont over index on this.
    
if __name__ == "__main__":
    main()
