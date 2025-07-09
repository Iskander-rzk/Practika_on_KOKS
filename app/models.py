from pydantic import BaseModel
from typing import Optional

class IPAddress(BaseModel):
    id: Optional[int] = None
    ip_address: str
    description: Optional[str] = None