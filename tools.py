from dotenv import load_dotenv
import os
from pydantic import BaseModel, ValidationError
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.exceptions import OutputParserException
import asyncio
import logging
import json

from tools import search_tool, wiki_tool, save_tool

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
llm = ChatAnthropic(model=ANTHROPIC_MODEL, temperature=0.2, streaming=True)

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an advanced AI research assistant designed to generate comprehensive and well-structured research papers.
            Your primary goal is to answer the user's query thoroughly by effectively utilizing the provided tools (web search, Wikipedia, file save).

            Strictly adhere to the following output format. Provide no other text or conversational filler outside of this JSON structure.
            If a tool is used, make sure to list it in 'tools_used'.
            If no specific tools were explicitly used, you can leave 'tools_used' as an empty list or specify 'internal_knowledge'.

            {format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, save_tool]

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

async def run_research_agent(query: str) -> ResearchResponse | None:
    logger.info(f"Starting research for query: '{query}'")
    raw_response = None
    structured_response = None

    try:
        print("\n--- Agent Thinking... This may take a moment ---")
        result = await agent_executor.ainvoke({"query": query, "chat_history": []})
        
        raw_response = result.get("output")
        logger.info(f"Agent raw output received: {raw_response}")

        if isinstance(raw_response, str):
            try:
                json_data = json.loads(raw_response)
                structured_response = parser.parse(json_data)
            except (json.JSONDecodeError, ValidationError) as e:
                logger.error(f"Error parsing JSON or validating Pydantic model from string output: {e}")
                logger.error(f"Raw string output: {raw_response}")
                print(f"\n! Error: Could not fully parse the AI's response into the expected format.")
                print(f"  Attempting a partial or raw display. Details: {e}")
                print(f"\n--- Raw Agent Output ---\n{raw_response}")
                return None
        elif isinstance(raw_response, dict):
            try:
                structured_response = parser.parse(raw_response)
            except ValidationError as e:
                logger.error(f"Pydantic validation error for dict output: {e}")
                logger.error(f"Raw dict output: {raw_response}")
                print(f"\n! Error: AI's response did not match the expected structure.")
                print(f"  Details: {e}")
                print(f"\n--- Raw Agent Output ---\n{raw_response}")
                return None
        else:
            logger.warning(f"Unexpected raw_response type: {type(raw_response)}. Value: {raw_response}")
            print(f"\n! Warning: The AI returned an unexpected type of response.")
            print(f"  Raw response: {raw_response}")
            return None

    except OutputParserException as e:
        logger.error(f"LangChain OutputParserException: {e}")
        logger.error(f"Raw response leading to error: {raw_response}")
        print(f"\n! Error: The AI's response format was unexpected, leading to a parsing error.")
        print(f"  Details: {e}")
        print(f"  Raw response (if available): {raw_response}")
        return None
    except Exception as e:
        logger.exception(f"An unexpected error occurred during agent execution for query '{query}': {e}")
        print(f"\n! An unexpected error occurred during research: {e}")
        print(f"  Please check the logs for more details.")
        return None
    
    return structured_response

async def main():
    print("Welcome to the AI Research Assistant!")
    print("Type 'exit' to quit.")

    while True:
        query = input("\nWhat can I help you research today? ")
        if query.lower() == 'exit':
            print("Exiting research assistant. Goodbye!")
            break

        if not query.strip():
            print("Please enter a non-empty query.")
            continue

        response = await run_research_agent(query)

        if response:
            print("\n--- Research Complete! ---")
            print(f"Topic: {response.topic}")
            print(f"Summary:\n{response.summary}")
            print(f"Sources: {', '.join(response.sources) if response.sources else 'None'}")
            print(f"Tools Used: {', '.join(response.tools_used) if response.tools_used else 'None'}")
            
            save_confirm = input("\nWould you like to save this research to a file? (yes/no): ").lower()
            if save_confirm == 'yes':
                try:
                    json_output = response.model_dump_json(indent=2)
                    save_tool.run(json_output)
                    print("Research successfully saved to research_output.txt.")
                except Exception as e:
                    logger.error(f"Failed to save structured response: {e}")
                    print(f"Error saving research: {e}")
        else:
            print("\nResearch could not be completed or parsed successfully.")
            print("Please review the logs for more information.")

if __name__ == "__main__":
    asyncio.run(main())
