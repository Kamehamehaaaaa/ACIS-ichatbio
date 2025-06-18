from typing import override, Optional, AsyncGenerator, AsyncIterator

from pydantic import BaseModel

from ichatbio.agent import IChatBioAgent
from ichatbio.types import AgentCard, Message
from entrypoints import get_occurrence

class OBISAgent(IChatBioAgent):

    @override
    def get_agent_card(self) -> AgentCard:
        return AgentCard(
            name="Ocean Biodiversity Information Systems data source",
            description="Retrieves data from OBIS (https://api.obis.org).",
            icon=None,
            entrypoints=[
                get_occurrence.entrypoint
            ]
        )

    @override
    async def run(self, request: str, entrypoint: str, params: Optional[BaseModel]) -> AsyncGenerator[None, Message]:
        coro: AsyncIterator[Message]
        match entrypoint:
            case get_occurrence.entrypoint.id:
                coro = get_occurrence.run(request)
            case _:
                raise ValueError()

        async for message in coro:
            yield message