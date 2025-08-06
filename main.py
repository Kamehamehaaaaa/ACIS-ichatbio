from agent import OBISAgent
import asyncio
from ichatbio.server import run_agent_server
from ichatbio.agent_response import ResponseChannel, ResponseContext, ResponseMessage

class InMemoryResponseChannel(ResponseChannel):
    """
    Useful for interacting with agents locally (e.g., unit tests, command line interfaces) instead of sending responses
    over the network. The `message_buffer` is populated by running an agent.

    Example:

        messages = list()
        channel = InMemoryResponseChannel(messages)
        context = ResponseContext(channel)

        # `messages` starts empty
        agent = HelloWorldAgent()
        await agent.run(context, "Hi", "hello", None)
        # `messages` should now be populated

        assert messages[1].text == "Hello world!"
    """

    def __init__(self, message_buffer: list):
        self.message_buffer = message_buffer

    async def submit(self, message: ResponseMessage, context_id: str):
        self.message_buffer.append(message)

async def main():
    agent = OBISAgent()
    messages = list()
    channel = InMemoryResponseChannel(messages)
    context = ResponseContext(channel, "617727d1-4ce8-4902-884c-db786854b51c")    
    userInput = input()
    await agent.run(context, userInput, "get_occurrence", None)
    # messages1 = [m async for m in response]
    print(messages)

agent = OBISAgent()
run_agent_server(agent, "0.0.0.0", 8989)
# userInput = input("Enter Search Query: \n")
# asyncio.run(main())

