from typing import Dict, Any, Optional, List
from pydantic import BaseModel

from models.ArtistInfo import ArtistInfo

class ArtResearchState(BaseModel):
    query: str
    
    extracted_artworks: List[str] = []
    artists: List[ArtistInfo] = []
    
    search_results: List[Dict[str, Any]] = []
    analysis: Optional[str] = None