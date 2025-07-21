from fastapi import APIRouter, Request
from app.crud import crud
from app.core.templates import templates
router = APIRouter()
from app.controller.controller import get_current_user

@router.get("/")
async def read_root(request: Request):
    ip_addresses = crud.get_all_ip_addresses()
    message = request.query_params.get("message", "")
    error = request.query_params.get("error", "")
    current_user = get_current_user(request)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "ip_addresses": ip_addresses,
            "message": message,
            "error": error,
            "current_user": current_user.username if current_user else None
        }
    )