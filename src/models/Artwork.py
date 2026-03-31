from pydantic import BaseModel
from typing import List, Optional

class Artwork(BaseModel):
    title: str
    artist: str
    year: Optional[int] = None
    
    style: Optional[str] = None
    medium: Optional[str] = None
    
    description: str = ""
    tags: List[str] = []
    
    image_url: Optional[str] = None
    museum: Optional[str] = None