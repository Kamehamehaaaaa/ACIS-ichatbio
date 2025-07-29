from typing import override, Optional, AsyncGenerator, AsyncIterator

from pydantic import BaseModel

from ichatbio.agent import IChatBioAgent
from ichatbio.types import AgentCard
from entrypoints import get_occurrence, checklist

from ichatbio.agent_response import ResponseContext, IChatBioAgentProcess

class OBISAgent(IChatBioAgent):

    @override
    def get_agent_card(self) -> AgentCard:
        return AgentCard(
            name="Ocean Biodiversity Information Systems data source",
            description="Retrieves data from OBIS (https://api.obis.org).",
            icon=None,
            entrypoints=[
                get_occurrence.entrypoint,
                checklist.entrypoint
            ]
        )

    @override
    async def run(self, context: ResponseContext, request: str, entrypoint: str, params: Optional[BaseModel]):
        match entrypoint:
            case get_occurrence.entrypoint.id:
                await get_occurrence.run(request, context)
            case checklist.entrypoint.id:
                await checklist.run(request, context)
            case _:
                raise ValueError()
        await context.reply("OBIS query completed")