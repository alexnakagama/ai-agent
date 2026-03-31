from typing import Dict

from langgraph.graph import StateGraph, END

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from src.firecrawl import FirecrawlService

from src.models.ArtAnalysis import ArtAnalysis
from src.models.ArtistInfo import ArtistInfo
from src.models.ArtResearchState import ArtResearchState
from src.models.Artwork import Artwork

from src.prompts import ArtPrompts

class Workflow:
    def __init__(self):
        self.firecrawl = FirecrawlService()
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        self.prompts = ArtPrompts()
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        pass

    