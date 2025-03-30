import logging
from src.sierra_agents import triage_agent
from src.tools import SierraOutfittersAgentContext
from agents import (
    HandoffOutputItem,
    ItemHelpers,
    MessageOutputItem,
    Runner,
    ToolCallItem,
    ToolCallOutputItem
)


class AgentRunner:
    def __init__(self, default_agent=triage_agent, context=None):
        self.default_agent = default_agent
        self.context = context or SierraOutfittersAgentContext()
        self.logger = logging.getLogger(__name__)
    
    async def run(self):
        current_agent = self.default_agent
        input_items = []

        while True:
            user_input = input("Enter your message: ")
            input_items.append({"content": user_input, "role": "user"})
            result = await Runner.run(current_agent, input_items, context=self.context)

            for new_item in result.new_items:
                agent_name = new_item.agent.name
                if isinstance(new_item, MessageOutputItem):
                    print(ItemHelpers.text_message_output(new_item))
                    self.logger.info(f"{agent_name}: {ItemHelpers.text_message_output(new_item)}")
                elif isinstance(new_item, HandoffOutputItem):
                    self.logger.info(f"Handed off from {new_item.source_agent.name} to {new_item.target_agent.name}")
                elif isinstance(new_item, ToolCallItem):
                    self.logger.info(f"{agent_name}: Calling a tool")
                elif isinstance(new_item, ToolCallOutputItem):
                    self.logger.info(f"{agent_name}: Tool call output: {new_item.output}")
                else:
                    self.logger.info(f"{agent_name}: Skipping item: {new_item.__class__.__name__}")
            input_items = result.to_input_list()
            current_agent = result.last_agent
