from typing import List, Optional
from pydantic import BaseModel

class ArtAnalysis(BaseModel):
    """Structured output for LLM analysis of artworks or artists"""
    
    style: str  # Impressionism, Abstract, Realism, Digital, etc.
    medium: Optional[str] = None  # Oil, Acrylic, Digital, Sculpture, etc.
    themes: List[str] = []  # Nature, Identity, Politics, etc.
    description: str = ""
    
    period: Optional[str] = None  # Renaissance, Modern, Contemporary
    influences: List[str] = []
    techniques: List[str] = []