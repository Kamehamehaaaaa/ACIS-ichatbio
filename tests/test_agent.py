import pytest
from ichatbio.types import ArtifactMessage, ProcessMessage

from agent import OBISAgent


@pytest.mark.asyncio
async def test_idigbio():
    agent = OBISAgent()
    response = agent.run("Retrieve records of Egregia menziesii", "get_occurrence", None)
    messages = [m async for m in response]

    process_messages: list[ProcessMessage] = [p for p in messages if type(p) is ProcessMessage]
    assert len(process_messages) == 4

    search_parameters = next(p.data for p in process_messages if p.description == "Generated search parameters")
    assert search_parameters == {
        "scientificname": "Egregia menziesii",
    }

    artifacts = [p for p in messages if type(p) is ArtifactMessage]
    assert len(artifacts) == 1

    artifact: ArtifactMessage = artifacts[0]
    assert artifact.mimetype == "application/json"
    assert artifact.uris
    assert artifact.metadata["data_source"] == "OBIS"
