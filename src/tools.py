import logging
from agents import function_tool, RunContextWrapper
from pydantic import BaseModel

from src.services.product import Product
from src.services.order import Order

logger = logging.getLogger(__name__)


class SierraOutfittersAgentContext(BaseModel):
    email: str | None = None
    order_number: str | None = None


# Triage tools
@function_tool
def capture_email_or_order_number(context: RunContextWrapper[SierraOutfittersAgentContext], email: str = None, order_number: str = None) -> None:
    if email is not None:
        context.context.email = email
        logger.info(f"Stored email in context: {email}")
    if order_number is not None:
        context.context.order_number = order_number
        logger.info(f"Stored order number in context: {order_number}")


# Products Tools
@function_tool
def product_descriptions() -> str:
    logger.info("Tool called: product_descriptions")
    product_helper = Product()
    return product_helper.product_descriptions()


@function_tool
def products_availablity(context: RunContextWrapper[SierraOutfittersAgentContext], product_skus: list[str]) -> str:
    """Given a list of SKUs find the number of units available.

    Args:
        product_skus (list[str]): List of SKUs to search, follows #W000 format, make sure to include the leading #
    """
    logger.info(f"Tool called: products_availablity with SKUs: {product_skus}")
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
    logger.info(f"Tool called: fetch_orders with email: {email}")
    
    if email is None and context.context.email is None:
        logger.warning("No email provided and none in context")
    
    order_helper = Order()
    email = email or context.context.email
    context.context.email = email
    logger.info(f"Looking up orders for email: {email}")

    order_numbers = order_helper.order_numbers(email)
    if order_numbers:
        context.context.order_number = order_numbers[0]
        logger.info(f"Found and stored first order number in context: {order_numbers[0]}")
    else:
        logger.warning(f"No orders found for email: {email}")
        
    return order_numbers


@function_tool
def order_status(context: RunContextWrapper[SierraOutfittersAgentContext], order_number: str = None):
    """Get the status of an order by its order number.
    
    Args:
        context (RunContextWrapper[SierraOutfittersAgentContext]): Context wrapper
        order_number (str, optional): Order number to look up. If None, will use context. Defaults to None.
        
    Returns:
        str: Status and details of the order
    """
    logger.info(f"Tool called: order_status with order_number: {order_number}")
    
    if order_number is None and context.context.order_number is None:
        logger.warning("No order number provided and none in context")
    
    order_helper = Order()
    order_number = order_number or context.context.order_number
    context.context.order_number = order_number
    logger.info(f"Looking up status for order: {order_number}")

    return order_helper.order_status(order_number)
