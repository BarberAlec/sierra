from agents import function_tool, RunContextWrapper
from pydantic import BaseModel

from src.services.product import Product
from src.services.order import Order


class SierraOutfittersAgentContext(BaseModel):
    email: str | None = None
    order_number: str | None = None


# Triage tools
@function_tool
def capture_email_or_order_number(context: RunContextWrapper[SierraOutfittersAgentContext], email: str = None, order_number: str = None) -> None:
    if email is not None:
        context.context.email = email
    if order_number is not None:
        context.context.order_number = order_number


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
def fetch_orders(context: RunContextWrapper[SierraOutfittersAgentContext], email: str = None) -> str:
    """Fetch order numbers for a given email, if none provided we will use stored context to see if we have an email for this user.
    If we do not you will have to call this tool again with an email.

    Args:
        context (RunContextWrapper[SierraOutfittersAgentContext]): Context wrapper
        email (str, optional): email address to search order numbers against. Defaults to None.

    Returns:
        str: an order number for this email
    """
    order_helper = Order()
    email = email or context.context.email
    context.context.email = email

    order_numbers = order_helper.order_numbers(email)
    if order_numbers:
        context.context.order_number = order_numbers[0]
    return order_numbers


@function_tool
def order_status(context: RunContextWrapper[SierraOutfittersAgentContext], order_number: str = None):
    order_helper = Order()
    order_number = order_number or context.context.order_number
    context.context.order_number = order_number

    return order_helper.order_status(order_number)
