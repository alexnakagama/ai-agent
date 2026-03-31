from pydantic import BaseModel
from typing import List, Optional

class ArtistInfo(BaseModel):
    name: str
    bio: str
    
    nationality: Optional[str] = None
    birth_year: Optional[int] = None
    
    styles: List[str] = []
    mediums: List[str] = []
    
    notable_works: List[str] = []
    influences: List[str] = []
    
    website: Optional[str] = None