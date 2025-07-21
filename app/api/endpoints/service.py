from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import RedirectResponse
from app.controller import controller
from app.controller.controller import get_current_user

router = APIRouter()

@router.post("/export/")
async def export_ips(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/user/login/", status_code=303)

    response = controller.export_ips()
    return RedirectResponse(
        url=f"/user/{user.id}/?message=IPs+exported" if not response.error else f"/user/{user.id}/?error={response.error.string()}",
        status_code=303
    )

@router.post("/import/")
async def import_ips(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/user/login/", status_code=303)

    response = controller.import_ips()
    return RedirectResponse(
        url=f"/user/{user.id}/?message=IPs+imported" if not response.error else f"/user/{user.id}/?error={response.error.string()}",
        status_code=303
    )

@router.post("/upload/")
async def upload_file(request: Request, file: UploadFile = File(...)):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/user/login/", status_code=303)

    response = controller.upload_and_import(file)
    return RedirectResponse(
        url=f"/user/{user.id}/?message=File+uploaded" if not response.error else f"/user/{user.id}/?error={response.error.string()}",
        status_code=303
    )