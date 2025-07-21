import os
from app.crud import crud
from app.models import models
from fastapi import UploadFile, Request
import secrets
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
IP_FILE_PATH = "ip_addresses.txt"


def add_ip(input: models.IPAddressRequest) -> models.IPAddressResponse:
    if not input.is_valid():
        return models.IPAddressResponse(error=models.Errors.Invalid)
    if crud.select(input.ip_address):
        return models.IPAddressResponse(error=models.Errors.Exist)
    if not crud.create_ip_address(input.ip_address):
        return models.IPAddressResponse(error=models.Errors.DBError)
    return models.IPAddressResponse()


def add_ip_for_handler(input: models.IPAddressRequest) -> models.IPAddressResponse:
    result = add_ip(input)
    if not result.error:
        result.ip_addresses = crud.get_all_ip_addresses()
    return result


def search_ip(ip: str) -> models.IPAddressResponse:
    temp_request = models.IPAddressRequest(ip_address=ip)
    if not temp_request.is_valid():
        all_ips = crud.get_all_ip_addresses()
        return models.IPAddressResponse(
            error=models.Errors.Invalid,
            ip_addresses=all_ips
        )
    results = crud.search_ip_addresses(ip)
    return models.IPAddressResponse(ip_addresses=results)


def remove_ip(ip_address: str) -> models.IPAddressResponse:
    success = crud.delete_ip_address(ip_address)
    if not success:
        return models.IPAddressResponse(error=models.Errors.DBError)
    ip_addresses = crud.get_all_ip_addresses()
    return models.IPAddressResponse(ip_addresses=ip_addresses)


def export_ips() -> models.OperationResponse:
    ip_addresses = crud.get_all_ip_addresses()
    with open(IP_FILE_PATH, "w") as f:
        for ip in ip_addresses:
            f.write(f"{ip.ip_address}\n")
    return models.OperationResponse(message="Export successful")


def import_ips() -> models.OperationResponse:
    if not os.path.exists(IP_FILE_PATH):
        return models.OperationResponse(error=models.Errors.Invalid)


    with open(IP_FILE_PATH, 'r') as f:
        for line in f:
            ip = line.strip()
            if ip:
                add_ip_for_handler(models.IPAddressRequest(ip_address=ip))
    ip_addresses=crud.get_all_ip_addresses()

    return models.OperationResponse(message="Import successful", ip_addresses=ip_addresses)


def upload_and_import(file: UploadFile) -> models.OperationResponse:
    content = file.file.read()
    for line in content.decode('utf-8').splitlines():
        ip = line.strip()
        if ip:
            add_ip_for_handler(models.IPAddressRequest(ip_address=ip))
    ip_addresses=crud.get_all_ip_addresses()

    return models.OperationResponse(message="Upload completed", ip_addresses=ip_addresses)




SESSION_TOKEN_LENGTH = 32
MIN_PASSWORD_LENGTH = 8


def get_current_user(request: Request) -> models.UserDB | None:
    session_token = request.cookies.get("session_token")
    if not session_token:
        return None
    return crud.get_user_by_session(session_token)


# Удалите эти строки:
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Измените функции регистрации и входа:
def register_user(user_data: models.UserRegister) -> models.AuthResponse:
    if crud.get_user_by_username(user_data.username):
        return models.AuthResponse(error=models.Errors.UserExists)

    if len(user_data.password) < MIN_PASSWORD_LENGTH:
        return models.AuthResponse(error=models.Errors.WeakPassword)

    # Сохраняем пароль в открытом виде (без хеширования)
    user = crud.create_user(user_data.username, user_data.password)
    if not user:
        return models.AuthResponse(error=models.Errors.DBError)

    return models.AuthResponse(message="Registration successful")

def login_user(user_data: models.UserLogin) -> models.AuthResponse:
    user = crud.get_user_by_username(user_data.username)
    if not user:
        return models.AuthResponse(error=models.Errors.InvalidCredentials)

    if user_data.password != user.password_hash:  # Без хеширования
        return models.AuthResponse(error=models.Errors.InvalidCredentials)

    session_token = secrets.token_hex(SESSION_TOKEN_LENGTH)
    if not crud.create_session(user.id, session_token):
        return models.AuthResponse(error=models.Errors.DBError)

    return models.AuthResponse(message=session_token, user=user)  # Добавляем user в ответ