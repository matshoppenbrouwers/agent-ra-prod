from pydantic import BaseModel
from typing import List

class Framework(BaseModel):
    name: str
    description: str
    scientific_basis: str
    key_proponents: List[str]
    practical_applications: List[str]
    implementation_requirements: List[str]
    limitations: List[str] 