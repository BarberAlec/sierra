from agents import Agent, WebSearchTool

from src.tools import (
    fetch_orders,
    order_status,
    products_availablity,
    product_descriptions,
    capture_email_or_order_number,
    SierraOutfittersAgentContext
    )
from src.prompts import Prompts


MODEL = "gpt-4o-mini"


order_prompt = Prompts('order')
orders_agent = Agent[SierraOutfittersAgentContext](
    model=MODEL,
    name="Product Orders Agent",
    handoff_description=order_prompt.handoff(),
    instructions=order_prompt.prompt(),
    tools=[fetch_orders, order_status],
)

product_prompt = Prompts('product')
products_agent = Agent[SierraOutfittersAgentContext](
    model=MODEL,
    name="Product Information Agent",
    handoff_description=product_prompt.handoff(),
    instructions=product_prompt.prompt(),
    tools=[product_descriptions, products_availablity],
)

hiking_prompt = Prompts('hiking')
hiking_agent = Agent[SierraOutfittersAgentContext](
    model=MODEL,
    name="Hiking Questions and Advice Agent",
    handoff_description=hiking_prompt.handoff(),
    instructions=hiking_prompt.prompt(),
    tools=[WebSearchTool()],
)

triage_prompt = Prompts('triage')
triage_agent = Agent[SierraOutfittersAgentContext](
    name="Triage Agent",
    model=MODEL,
    handoff_description=triage_prompt.handoff(),
    instructions=triage_prompt.prompt(),
    tools=[capture_email_or_order_number],
    handoffs=[
        orders_agent,
        products_agent,
        hiking_agent
    ],
)
orders_agent.handoffs.append(triage_agent)
products_agent.handoffs.append(triage_agent)
hiking_agent.handoffs.append(triage_agent)
