from agents import function_tool, RunContextWrapper
from pydantic import BaseModel

from src.services.product import Product
from src.services.order import Order


class SierraOutfittersAgentContext(BaseModel):
    email: str | None = None
    name: str | None = None
    order_numbers: list[str] | None = None


# Products Tools
@function_tool
def product_descriptions() -> str:
    product_helper = Product()
    return product_helper.product_descriptions()


@function_tool
def products_availablity(context: RunContextWrapper[SierraOutfittersAgentContext], product_skus: list[str]) -> str:
    """Given a list of SKUs find the number of units available.

    Args:
        product_skus (list[str]): List of SKUs to search, follows #W000 format, make sure to include the leading #
    """
    product_helper = Product()
    return product_helper.availablity(product_skus)


# Orders tools
@function_tool
def fetch_orders(context: RunContextWrapper[SierraOutfittersAgentContext], email: str):
    order_helper = Order()
    context.context.order_numbers = order_helper.order_numbers(email)
    context.context.email = email
    return context.context.order_numbers


@function_tool
def order_status(context: RunContextWrapper[SierraOutfittersAgentContext], order_number: str):
    order_helper = Order()
    return order_helper.order_status(order_number)
