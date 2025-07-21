import enum
import ipaddress
from pydantic import BaseModel
from typing import List, Optional

class IPAddressDB(BaseModel):
    id: Optional[int] = None
    ip_address: str

class IPAddressRequest(BaseModel):
    ip_address: str

    def is_valid(self) -> bool:
        if not self.ip_address:
            return True
        try:
            if ']:' in self.ip_address:
                ip_part = self.ip_address.split(']:', 1)[0] + ']'
                ipaddress.ip_address(ip_part[1:])
            elif ':' in self.ip_address:
                ip_part = self.ip_address.rsplit(':', 1)[0]
                ipaddress.ip_address(ip_part)
            else:
                ipaddress.ip_address(self.ip_address)
            return True
        except ValueError:
            allowed_chars = set("0123456789.:abcdefABCDEF")
            return all(char in allowed_chars for char in self.ip_address)

class Errors(enum.Enum):
    Invalid = 1
    Exist = 2
    DBError = 3
    UserExists = 4
    WeakPassword = 5
    InvalidCredentials = 6

    def string(self) -> str:
        error_messages = {
            Errors.Invalid: "Invalid IP address",
            Errors.Exist: "IP address exists",
            Errors.DBError: "Database error",
            Errors.UserExists: "Username already exists",
            Errors.WeakPassword: "Password must be at least 8 characters",
            Errors.InvalidCredentials: "Invalid username or password"
        }
        return error_messages.get(self, "Unknown error")

class IPAddressResponse(BaseModel):
    error: Optional[Errors] = None
    ip_addresses: List[IPAddressDB] = []

class OperationResponse(BaseModel):
    error: Optional[Errors] = None
    message: Optional[str] = None
    ip_addresses: List[IPAddressDB] = []

class UserDB(BaseModel):
    id: Optional[int] = None
    username: str
    password_hash: str

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    error: Optional[Errors] = None
    message: Optional[str] = None
    user: Optional[UserDB] = None
    token: Optional[str] = None