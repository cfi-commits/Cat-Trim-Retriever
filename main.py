from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import ADMIN_PASSWORD
from dropbox_client import get_trim_file
from logging_utils import log_request, fetch_logs

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "error": None,
        },
    )


@app.post("/retrieve")
async def retrieve_file(
    request: Request,
    part_number: str = Form(...),
    serial_number: str = Form(...),
):
    client_ip = request.client.host if request.client else "unknown"

    try:
        filename, data = get_trim_file(part_number, serial_number)
        log_request(
            part_number=part_number,
            serial_number=serial_number,
            client_ip=client_ip,
            success=True,
            message="File retrieved",
        )
        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
        return Response(
            content=data,
            media_type="application/octet-stream",
            headers=headers,
        )
    except FileNotFoundError as e:
        log_request(
            part_number=part_number,
            serial_number=serial_number,
            client_ip=client_ip,
            success=False,
            message=str(e),
        )
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": "File not found. Please check the part number and serial number.",
            },
        )
    except Exception as e:
        log_request(
            part_number=part_number,
            serial_number=serial_number,
            client_ip=client_ip,
            success=False,
            message=f"Unexpected error: {e}",
        )
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": "An unexpected error occurred while retrieving the file.",
            },
        )


@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    return templates.TemplateResponse(
        "admin_logs.html",
        {
            "request": request,
            "authorized": False,
            "logs": [],
            "error": None,
        },
    )


@app.post("/admin", response_class=HTMLResponse)
async def admin_view_logs(
    request: Request,
    password: str = Form(...),
):
    if password != ADMIN_PASSWORD:
        return templates.TemplateResponse(
            "admin_logs.html",
            {
                "request": request,
                "authorized": False,
                "logs": [],
                "error": "Invalid password.",
            },
        )

    logs = fetch_logs()
    return templates.TemplateResponse(
        "admin_logs.html",
        {
            "request": request,
            "authorized": True,
            "logs": logs,
            "error": None,
        },
    )