from tortoise import fields
from tortoise.models import Model


class Session(Model):
    """Список загруженных сессий"""
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, default=None, unique=True)
    api_id = fields.IntField(null=True)
    api_hash = fields.CharField(null=True, max_length=255)
    category = fields.CharField(default="базовая", max_length=255)
    active = fields.BooleanField(default=False)
    banned = fields.BooleanField(default=False)
    banned_until = fields.DatetimeField(null=True)
    reactivate = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    session_string = fields.CharField(max_length=2048)

    # Базовые данные сессии
    base_name = fields.CharField(max_length=70, null=True, default=None)
    base_surname = fields.CharField(max_length=70, null=True, default=None)
    base_status = fields.CharField(max_length=70, null=True, default=None)
    base_photo = fields.CharField(max_length=128, null=True, default=None)

    channels = fields.JSONField(null=True)

    class Meta:
        table = "session"
