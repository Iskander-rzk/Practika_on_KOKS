from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from app.controller import controller
from app.controller.controller import get_current_user
from app.crud.crud import search_ip_addresses
from app.models.models import IPAddressRequest

router = APIRouter()

@router.post("/add/")
async def add_ip_address(request: Request, ip: str = Form(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/user/login/", status_code=303)

    result = controller.add_ip(IPAddressRequest(ip_address=ip))
    return RedirectResponse(
        url=f"/user/{user.id}/?message=IP+added" if not result.error else f"/user/{user.id}/?error={result.error.string()}",
        status_code=303
    )

@router.get("/search")
async def search_ips(request: Request, ip: str = ""):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/user/login", status_code=303)

    # Перенаправляем с search_term на страницу пользователя
    return RedirectResponse(
        url=f"/user/{user.id}?search_term={ip}",
        status_code=303
    )

@router.post("/delete/{ip_address}/")
async def remove_ip_address(request: Request, ip_address: str):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/user/login/", status_code=303)

    response = controller.remove_ip(ip_address)
    return RedirectResponse(
        url=f"/user/{user.id}/?message=IP+deleted" if not response.error else f"/user/{user.id}/?error={response.error.string()}",
        status_code=303
    )