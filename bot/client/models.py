from tortoise import fields
from tortoise.models import Model


class Client(Model):
    """Базовая модель клиента (не включает админов и модераторов)"""
    telegram_username = fields.CharField(max_length=255, unique=True)
    telegram_id = fields.BigIntField(pk=True, unique=True)
    register_data = fields.DatetimeField(auto_now_add=True)
    register_until = fields.DatetimeField(null=True)
    post_limit = fields.IntField(default=1)
    is_blocked = fields.BooleanField(default=False)
    allow_run = fields.BooleanField(default=True)
    allow_edit_session = fields.BooleanField(default=True)

    class Meta:
        table = "client"


class ClientAction(Model):
    id = fields.IntField(pk=True)
    log_data = fields.CharField(max_length=512)
    owner = fields.ForeignKeyField('models.Client', related_name='user_log',
                                   on_delete=fields.CASCADE)  # Владелец объявления
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "client_action"
