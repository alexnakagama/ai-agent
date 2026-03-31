<div align="center">

# Art Research AI Agent

**An intelligent art research assistant powered by LangGraph, LangChain, and Firecrawl.**  
Give it any art-related query and it will search the web, analyze artists and artworks, and return structured insights with a personalized recommendation.

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.1%2B-green?style=flat-square)](https://langchain-ai.github.io/langgraph/)
[![LangChain](https://img.shields.io/badge/LangChain-1.2%2B-blue?style=flat-square)](https://python.langchain.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com/)
[![Firecrawl](https://img.shields.io/badge/Firecrawl-4.21%2B-orange?style=flat-square)](https://firecrawl.dev/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.12%2B-E92063?style=flat-square)](https://docs.pydantic.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

</div>

---

## Overview

Art Research AI Agent is a **multi-step agentic workflow** that transforms a free-form question about art into structured, actionable insights. It orchestrates three sequential LLM-powered steps:

1. **Extract** — find relevant artists and artwork names from live web content.
2. **Research** — scrape pages for each entity and produce a structured `ArtAnalysis`.
3. **Recommend** — synthesize findings into a concise, personalized recommendation.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Workflow orchestration | [LangGraph](https://langchain-ai.github.io/langgraph/) `StateGraph` |
| LLM calls | [LangChain](https://python.langchain.com/) + [OpenAI](https://openai.com/) `gpt-4o-mini` |
| Web search & scraping | [Firecrawl](https://firecrawl.dev/) |
| Data validation | [Pydantic v2](https://docs.pydantic.dev/) |
| Configuration | [python-dotenv](https://pypi.org/project/python-dotenv/) |
| Runtime | Python 3.12+ |

---

## Project Structure

```
ai-agent/
├── main.py                      # CLI entry point
├── pyproject.toml               # Project metadata & dependencies
├── .env                         # API keys (not committed)
└── src/
    ├── workflow.py              # LangGraph workflow definition & step logic
    ├── firecrawl.py             # Firecrawl search & scrape service
    ├── prompts.py               # All LLM prompt templates
    └── models/
        ├── ArtResearchState.py  # LangGraph state schema
        ├── ArtistInfo.py        # Artist data model
        ├── ArtAnalysis.py       # Structured LLM output schema
        └── Artwork.py           # Artwork data model
```

---

## Workflow

The agent runs a **linear three-node graph** compiled by LangGraph:

```
[User Query]
     │
     ▼
┌────────────────────┐
│  extract_artworks  │  Search the web → scrape pages → LLM extracts names
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│     research       │  Per entity: search → scrape → LLM structured analysis
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│     recommend      │  LLM synthesizes all artists → final recommendation
└────────┬───────────┘
         │
         ▼
      [END]
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- An [OpenAI API key](https://platform.openai.com/api-keys)
- A [Firecrawl API key](https://firecrawl.dev/)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/ai-agent.git
cd ai-agent

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -e .
```

### Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-...
FIRECRAWL_API_KEY=fc-...
```

---

## Usage

```bash
python main.py
```

You will be prompted to enter an art research query:

```
Enter your art research query: surrealist painters influenced by dreams
```

**Sample output:**

```
Finding artworks/artists related to: surrealist painters influenced by dreams
Extracted: Salvador Dalí, René Magritte, Max Ernst, Frida Kahlo, Yves Tanguy
Researching: Salvador Dalí, René Magritte, Max Ernst, Frida Kahlo
  Analyzed: Salvador Dalí — Surrealism
  Analyzed: René Magritte — Surrealism
  Analyzed: Max Ernst — Surrealism / Dadaism
  Analyzed: Frida Kahlo — Magic Realism

--- Results ---

Salvador Dalí
  Styles: Surrealism
  Bio: Salvador Dalí was a Spanish surrealist artist renowned for his technical
       skill and striking dreamlike imagery.

René Magritte
  Styles: Surrealism
  Bio: Belgian surrealist René Magritte is known for thought-provoking images
       that challenge pre-conditioned perceptions of reality.

Recommendation:
Salvador Dalí's work is the quintessential starting point for exploring
dream-based surrealism — his hyper-detailed paintings fuse Freudian imagery
with technical mastery. Magritte complements this with quieter, philosophical
puzzles. Together they define the core of the movement.
```

More query examples:

```bash
# Explore a specific movement
Enter your art research query: abstract expressionist artists from New York

# Look up an artist
Enter your art research query: Yayoi Kusama and her infinity rooms

# Discover by theme
Enter your art research query: contemporary artists exploring identity and diaspora

# Mixed media / digital art
Enter your art research query: generative art and AI-assisted artwork
```

---

## Data Models

### `ArtResearchState`
The shared state object that flows through every graph node.

| Field | Type | Description |
|---|---|---|
| `query` | `str` | The original user query |
| `extracted_artworks` | `List[str]` | Names extracted by the first step |
| `artists` | `List[ArtistInfo]` | Fully researched artist objects |
| `search_results` | `List[Dict]` | Raw Firecrawl search results |
| `analysis` | `Optional[str]` | Final recommendation text |

### `ArtistInfo`

| Field | Type | Description |
|---|---|---|
| `name` | `str` | Artist or artwork name |
| `bio` | `str` | Short biography or description |
| `nationality` | `Optional[str]` | Country of origin |
| `birth_year` | `Optional[int]` | Year of birth |
| `styles` | `List[str]` | Artistic styles (e.g., Impressionism) |
| `mediums` | `List[str]` | Materials or formats used |
| `notable_works` | `List[str]` | Key works |
| `influences` | `List[str]` | Artistic influences |
| `website` | `Optional[str]` | Source URL |

### `ArtAnalysis`
Structured output schema for LLM-extracted analysis, used with `with_structured_output()`.

| Field | Type | Description |
|---|---|---|
| `style` | `str` | Artistic movement (e.g., Surrealism) |
| `medium` | `Optional[str]` | Material or format |
| `themes` | `List[str]` | Main conceptual themes |
| `description` | `str` | One-sentence summary |
| `period` | `Optional[str]` | Historical period |
| `influences` | `List[str]` | Related artists or movements |
| `techniques` | `List[str]` | Notable techniques |

---

## Key Components

### `Workflow` — `src/workflow.py`
Builds and runs the LangGraph `StateGraph`. Contains the three step methods:

| Method | Description |
|---|---|
| `_extract_artworks_step` | Web search + LLM extraction of artist / artwork names |
| `_analyze_content` | Calls `with_structured_output(ArtAnalysis)` for a single entity |
| `_research_step` | Iterates extracted names, scrapes each, builds `ArtistInfo` list |
| `_recommend_step` | Final synthesis prompt returning a recommendation string |

### `FirecrawlService` — `src/firecrawl.py`
Thin wrapper around the Firecrawl SDK.

| Method | Description |
|---|---|
| `search_companies(query, num_results)` | Full-web search, returns markdown-formatted results |
| `scrape_company_pages(url)` | Scrapes a single URL and returns its markdown content |

### `ArtPrompts` — `src/prompts.py`
Central store for all prompt templates, decoupled from workflow logic.

| Attribute / Method | Purpose |
|---|---|
| `ART_EXTRACTION_SYSTEM` | System prompt for name extraction step |
| `art_extraction_user()` | User prompt template for extraction |
| `ART_ANALYSIS_SYSTEM` | System prompt for artwork/artist analysis |
| `art_analysis_user()` | User prompt template for per-entity analysis |
| `RECOMMENDATIONS_SYSTEM` | System prompt for final recommendation |
| `recommendations_user()` | User prompt template for recommendation |

---

## License

This project is licensed under the [MIT License](LICENSE).