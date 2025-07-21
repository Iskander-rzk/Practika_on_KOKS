from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from app.core.templates import templates
from app.controller.controller import register_user, login_user, get_current_user, search_ip
from app.models import models
from app.crud import crud

router = APIRouter()


# 1. Сначала специальные маршруты (login/register)
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if get_current_user(request):
        user = get_current_user(request)
        return RedirectResponse(url=f"/user/{user.id}", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    response = login_user(models.UserLogin(username=username, password=password))
    if response.error:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": response.error.string(), "username": username}
        )

    redirect = RedirectResponse(url=f"/user/{response.user.id}", status_code=303)
    redirect.set_cookie(key="session_token", value=response.message)
    return redirect


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    if get_current_user(request):
        user = get_current_user(request)
        return RedirectResponse(url=f"/user/{user.id}", status_code=303)
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        confirm_password: str = Form(...)
):
    if password != confirm_password:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Passwords don't match", "username": username}
        )

    response = register_user(models.UserRegister(username=username, password=password))
    if response.error:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": response.error.string(), "username": username}
        )

    return RedirectResponse(url="/user/login?message=Registration+successful", status_code=303)


# 2. Общий маршрут с user_id должен быть ПОСЛЕ всех специальных маршрутов
@router.get("/{user_id}")
async def user_page(
        request: Request,
        user_id: int,
        search_term: str = "",
        message: str = "",
        error: str = ""
):
    current_user = get_current_user(request)
    if not current_user or current_user.id != user_id:
        return RedirectResponse(url="/user/login", status_code=303)

    # Получаем IP-адреса (с поиском или без)
    if search_term:
        ip_response = search_ip(search_term)
        ip_addresses = ip_response.ip_addresses
    else:
        ip_addresses = crud.get_all_ip_addresses()

    return templates.TemplateResponse(
        "user_dashboard.html",
        {
            "request": request,
            "current_user": current_user,
            "ip_addresses": ip_addresses,
            "search_term": search_term,
            "message": message,
            "error": error
        }
    )


@router.post("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("session_token")
    return response