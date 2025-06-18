from agent import OBISAgent
import asyncio

async def main():
    response = agent.run(userInput, "get_occurrence", None)
    messages = [m async for m in response]
    print(messages)

agent = OBISAgent()
userInput = input("Enter Search Query: \n")
asyncio.run(main())

