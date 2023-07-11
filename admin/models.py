from fastapi_admin.models import AbstractAdmin
from tortoise import fields, Model
import socks
import random


class Comment(Model):
    text = fields.TextField()


class Post(Model):
    name = fields.CharField(max_length=100)


class Proxy(Model):
    ip = fields.CharField(max_length=15)
    port = fields.CharField(max_length=5)
    username = fields.CharField(max_length=100, null=True)
    password = fields.CharField(max_length=100, null=True)

    def __str__(self) -> str:
        return f"{self.ip}:{self.port}"

    def to_socks(self) -> tuple:
        _ret = [socks.HTTP, self.ip, int(self.port)]
        if self.username:
            _ret.append(True)
            _ret.append(self.username)
        if self.password:
            _ret.append(self.password)
        return tuple(_ret)

    @classmethod
    async def get_available(cls):
        proxies = await Proxy.all()
        return random.choice(proxies)


class Account(Model):
    proxy = fields.ForeignKeyField("models.Proxy", related_name="accounts", null=True)
    api_key = fields.CharField(max_length=100)

    def __str__(self):
        return self.id

class Admin(AbstractAdmin):
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}#{self.username}"