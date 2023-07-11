from fastapi_admin.app import app
from fastapi_admin.resources import Link, Model, ToolbarAction, Field
from fastapi_admin.widgets import inputs
from fastapi_admin.file_upload import FileUpload
import os

from .models import Proxy, Account, Post, Comment

from starlette.requests import Request

from fastapi_admin.enums import Method
from fastapi_admin.i18n import _

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
upload = FileUpload(uploads_dir=os.path.join(BASE_DIR, "static", "uploads"))


@app.register
class Home(Link):
    label = "Home"
    icon = "fas fa-home"
    url = "/admin"


@app.register
class ProxyResource(Model):
    label = "Прокси"
    model = Proxy
    page_title = "Прокси"
    fields = [
        "id",
        "ip",
        "port",
        "username",
        "password",
    ]

    async def get_toolbar_actions(self, request: Request) -> list[ToolbarAction]:
        return [
            ToolbarAction(
                label=_("create"),
                icon="fas fa-plus",
                name="create",
                method=Method.GET,
                ajax=False,
                class_="btn-dark",
            ),
            ToolbarAction(
                label=_("import"),
                icon="fas fa-plus",
                name="import",
                method=Method.GET,
                ajax=False,
                class_="btn-success",
            ),
        ]


@app.register
class AccountResource(Model):
    label = "Аккаунты"
    model = Account
    page_title = "Аккаунты"
    fields = [
        "proxy",
        "api_key",
    ]


@app.register
class PostResource(Model):
    label = "Посты"
    model = Post
    page_title = "Отслеживаемые посты"
    fields = ["name"]


@app.register
class CommentResource(Model):
    label = "Комментарий"
    model = Comment
    page_title = "Текст комметария"
    fields = [
        "text",
    ]
