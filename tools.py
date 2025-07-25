from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def save_to_txt(data: str, filename: str = "research_output.txt") -> str:
    """
    Saves research data to a text file with a timestamp.
    Handles potential file writing errors.
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

        with open(filename, "a", encoding="utf-8") as f:
            f.write(formatted_text)
        logger.info(f"Data successfully saved to {filename}")
        return f"Data successfully saved to {filename}"
    except IOError as e:
        logger.error(f"Error saving data to file {filename}: {e}")
        return f"Error: Could not save data to file. {e}"
    except Exception as e:
        logger.error(f"An unexpected error occurred while saving data: {e}")
        return f"Error: An unexpected error occurred while saving data. {e}"

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file. Input should be the text content to save.",
)

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for current information using DuckDuckGo. Use this tool for up-to-date facts and general knowledge.",
)


api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper,
                              description="Query Wikipedia for detailed information and historical context. Provides a summary of the top result.")
