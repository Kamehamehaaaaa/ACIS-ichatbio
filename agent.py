from typing import override, Optional, AsyncGenerator, AsyncIterator

from pydantic import BaseModel

from ichatbio.agent import IChatBioAgent
from ichatbio.types import AgentCard
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
    async def run(self, context, request: str, entrypoint: str, params: Optional[BaseModel]):
        match entrypoint:
            case get_occurrence.entrypoint.id:
                await get_occurrence.run(request, context)
            case _:
                raise ValueError()