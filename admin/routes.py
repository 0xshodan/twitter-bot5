from fastapi import Depends
from starlette.requests import Request
from starlette.responses import RedirectResponse
from fastapi_admin.app import app
from fastapi_admin.depends import get_resources
from fastapi_admin.template import templates
from typing import Annotated
from .models import Proxy
from fastapi import Form, status


@app.get("/")
async def home(
    request: Request,
    resources=Depends(get_resources),
):
    return templates.TemplateResponse(
        "dashboard.html",
        context={
            "request": request,
            "resources": resources,
            "resource_label": "Просмотреть канал",
            "page_title": "Просмотреть канал",
        },
    )


@app.get("/proxy/import")
async def import_proxy_page(
    request: Request,
    resources=Depends(get_resources),
):
    return templates.TemplateResponse(
        "proxy.html",
        context={
            "request": request,
            "resources": resources,
            "resource_label": "Импортировать прокси",
            "page_title": "Импортировать прокси",
        },
    )


@app.post("/proxy/import")
async def import_proxy(
    request: Request,
    text: Annotated[str, Form()],
    resources=Depends(get_resources),
):
    raw_proxies = text.split("\r\n")
    proxies = []
    for raw_proxy in raw_proxies:
        data = raw_proxy.split(":")
        if len(data) == 3:
            username = data[0]
            password, ip = data[1].split("@")
            port = data[2]
            proxies.append(
                Proxy(ip=ip, port=port, username=username, password=password)
            )
        else:
            try:
                ip = data[0]
                port = data[1]
                proxies.append(Proxy(ip=ip, port=port))
            except Exception as ex:
                print(ex)
    await Proxy.bulk_create(proxies, ignore_conflicts=True)
    return RedirectResponse("/admin/proxy/list", status_code=status.HTTP_303_SEE_OTHER)