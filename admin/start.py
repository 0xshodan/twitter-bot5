from redis.asyncio.client import Redis
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from admin.models import Admin
import os
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()
app.mount("/admin", admin_app)


register_tortoise(
    app,
    config={
        "connections": {
            "default": "sqlite://db.sqlite3"
        },
        "apps": {
            "models": {
                "models": ["admin.models"],
                "default_connection": "default",
            }
        },
    },
    generate_schemas=True,
)


@app.on_event("startup")
async def startup():
    r = Redis(
        decode_responses=True,
        encoding="utf8",
    )
    await admin_app.configure(
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        template_folders=[os.path.join(BASE_DIR, "templates")],
        favicon_url="https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/favicon.png",
        providers=[
            UsernamePasswordProvider(
                login_logo_url="https://preview.tabler.io/static/logo.svg",
                admin_model=Admin,
            )
        ],
        redis=r,
    )
