from typing import Any, Dict

from langgraph.graph import StateGraph, END

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from src.firecrawl import FirecrawlService

from src.models.ArtAnalysis import ArtAnalysis
from src.models.ArtistInfo import ArtistInfo
from src.models.ArtResearchState import ArtResearchState

from src.prompts import ArtPrompts

class Workflow:
    def __init__(self):
        self.firecrawl = FirecrawlService()
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        self.prompts = ArtPrompts()
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        graph = StateGraph(ArtResearchState)
        graph.add_node("extract_artworks", self._extract_artworks_step)
        graph.add_node("research", self._research_step)
        graph.add_node("recommend", self._recommend_step)

        graph.set_entry_point("extract_artworks")
        graph.add_edge("extract_artworks", "research")
        graph.add_edge("research", "recommend")
        graph.add_edge("recommend", END)

        return graph.compile()

    def _extract_artworks_step(self, state: ArtResearchState) -> Dict[str, Any]:
        print(f"Finding artworks/artists related to: {state.query}")

        search_query = f"{state.query} artists artworks"
        search_result = self.firecrawl.search_companies(search_query, num_results=3)

        all_content = ""
        results = search_result.data if search_result is not None else []
        for result in results:
            url = result.get("url", "")
            scraped = self.firecrawl.scrape_company_pages(url)
            if scraped is not None and scraped.markdown:
                all_content += scraped.markdown[:1500] + "\n\n"

        messages = [
            SystemMessage(content=self.prompts.ART_EXTRACTION_SYSTEM),
            HumanMessage(content=self.prompts.art_extraction_user(state.query, all_content))
        ]

        try:
            response = self.llm.invoke(messages)
            content = response.content if isinstance(response.content, str) else ""
            artwork_names = [
                name.strip()
                for name in content.strip().split("\n")
                if name.strip()
            ]
            print(f"Extracted: {', '.join(artwork_names[:5])}")
            return {"extracted_artworks": artwork_names}
        except Exception as e:
            print(e)
            return {"extracted_artworks": []}

    def _analyze_content(self, name: str, content: str) -> ArtAnalysis:
        structured_llm = self.llm.with_structured_output(ArtAnalysis)

        messages = [
            SystemMessage(content=self.prompts.ART_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompts.art_analysis_user(name, content))
        ]

        try:
            analysis = structured_llm.invoke(messages)
            if isinstance(analysis, ArtAnalysis):
                return analysis
            return ArtAnalysis(**analysis)
        except Exception as e:
            print(e)
            return ArtAnalysis(
                style="Unknown",
                medium="Unknown",
                themes=[],
                description="Unknown",
                period="Unknown",
                influences=[],
                techniques=[]
            )

    def _research_step(self, state: ArtResearchState) -> Dict[str, Any]:
        artwork_names = state.extracted_artworks[:4] if state.extracted_artworks else []

        if not artwork_names:
            print("No artworks/artists found, searching directly...")
            search_result = self.firecrawl.search_companies(state.query, num_results=4)
            results = search_result.data if search_result is not None else []
            artwork_names = [
                result.get("metadata", {}).get("title", "Unknown")
                for result in results
            ]

        print(f"Researching: {', '.join(artwork_names)}")

        artists: list[ArtistInfo] = []
        for name in artwork_names:
            search_result = self.firecrawl.search_companies(
                f"{name} artist artwork", num_results=1
            )
            results = search_result.data if search_result is not None else []
            if not results:
                continue

            url = results[0].get("url", "")
            scraped = self.firecrawl.scrape_company_pages(url)
            content = ""
            if scraped is not None and scraped.markdown:
                content = scraped.markdown[:3000]

            analysis = self._analyze_content(name, content)

            artist = ArtistInfo(
                name=name,
                bio=analysis.description,
                styles=[analysis.style] if analysis.style != "Unknown" else [],
                mediums=[analysis.medium] if analysis.medium else [],
                notable_works=[],
                influences=analysis.influences,
                website=url,
            )
            artists.append(artist)
            print(f"  Analyzed: {name} — {analysis.style}")

        return {"artists": artists}

    def _recommend_step(self, state: ArtResearchState) -> Dict[str, Any]:
        if not state.artists:
            return {"analysis": "No artists or artworks found to recommend."}

        art_data = "\n".join(
            f"- {a.name}: styles={a.styles}, influences={a.influences}, bio={a.bio}"
            for a in state.artists
        )

        messages = [
            SystemMessage(content=self.prompts.RECOMMENDATIONS_SYSTEM),
            HumanMessage(content=self.prompts.recommendations_user(state.query, art_data))
        ]

        try:
            response = self.llm.invoke(messages)
            content = response.content if isinstance(response.content, str) else ""
            return {"analysis": content}
        except Exception as e:
            print(e)
            return {"analysis": "Could not generate recommendations."}

    def run(self, query: str) -> Dict[str, Any]:
        initial_state = ArtResearchState(query=query)
        result = self.workflow.invoke(initial_state)
        return result
