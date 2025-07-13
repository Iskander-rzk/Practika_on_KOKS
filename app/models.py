from enum import Enum
from pydantic import BaseModel
from typing import Optional

class Errors(Enum):
    Invalid = "Invalid"
    Exist = "Exists"
    DBError = "DatabaseError"

class IPAddressDB(BaseModel):
    id: int
    ip_address: str

class IPAddressRequest(BaseModel):
    ip_address: str
    port: int = 0

    def render(self) -> str:
        return f"{self.ip_address}:{self.port}" if self.port else self.ip_address

    def validate(self) -> bool:
        parts = self.ip_address.split('.')
        if len(parts) != 4:
            return False
        return all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)

class IPAddressResponse(BaseModel):
    success: bool
    error: Optional[Errors] = None
    message: Optional[str] = None