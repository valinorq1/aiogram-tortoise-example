from tortoise import fields
from tortoise.models import Model


class EnterSession(Model):
    """Список сессий которые вступают в группы"""
    id = fields.IntField(pk=True)
    # имя которое будет отображаться в админ панели бота
    name = fields.CharField(max_length=255, default=None, unique=True)
    api_id = fields.IntField(null=True)
    api_hash = fields.CharField(null=True, max_length=255)
    # список каналов, в которые нужно вступить.
    channels = fields.JSONField(null=True, default=None)
    active = fields.BooleanField(default=False)
    finish = fields.BooleanField(default=False)
    category = fields.CharField(default="базовая", max_length=64)
    created_at = fields.DatetimeField(auto_now_add=True)
    session_string = fields.CharField(max_length=2048)
    # Базовые данные сессии
    base_name = fields.CharField(max_length=70, null=True, default=None)
    base_surname = fields.CharField(max_length=70, null=True, default=None)
    base_status = fields.CharField(max_length=70, null=True, default=None)
    base_photo = fields.CharField(max_length=128, null=True, default=None)

    class Meta:
        table = 'enter_session'
