from openai import AsyncOpenAI
import prompt_helper as prompt
import utils as utils
import instructor
from ichatbio.types import AgentEntrypoint

async def _generate_search_parameters(request: str, entrypoint: AgentEntrypoint, returnModel):
    system_prompt = prompt.build_system_prompt(entrypoint.id)
        
    client = AsyncOpenAI(api_key=utils.getValue("OPEN_API_KEY"), base_url=utils.getValue("OPENAI_BASE_URL"))
    
    instructor_client = instructor.patch(client)

    req = await instructor_client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=returnModel,
        messages=[
            {"role": "system",
                "content": system_prompt},
            {"role": "user", "content": request}],
        temperature=0,
    )

    generation = req.model_dump(exclude_none=True, by_alias=True)
    return generation