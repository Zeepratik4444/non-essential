import logging
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)

class DuckDuckGoSearchInput(BaseModel):
    search_query: str = Field(..., description="The query to search the web for.")
    max_results: int = Field(default=5, description="Maximum number of results to return.")

class DuckDuckGoSearchTool(BaseTool):
    """
    Search the web using DuckDuckGo.
    Useful for finding current information or discovering skill URLs.
    """
    name: str = "duckduckgo_search"
    description: str = (
        "A search tool that uses DuckDuckGo to find information on the internet. "
        "Useful for searching for skill definitions on skills.sh or GitHub. "
        "Example query: 'site:skills.sh code-review'"
    )
    args_schema: Type[BaseModel] = DuckDuckGoSearchInput

    def _run(self, search_query: str, max_results: int = 5) -> str:
        try:
            results = []
            with DDGS() as ddgs:
                ddgs_gen = ddgs.text(search_query, max_results=max_results)
                for r in ddgs_gen:
                    results.append(f"Title: {r['title']}\nURL: {r['href']}\nBody: {r['body']}\n")
            
            if not results:
                return f"No results found for query: {search_query}"
            
            return "\n---\n".join(results)
        except Exception as e:
            logger.error(f"Error searching DuckDuckGo: {e}")
            return f"❌ Error searching DuckDuckGo: {e}"
