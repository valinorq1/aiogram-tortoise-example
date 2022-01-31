from tortoise import fields
from tortoise.models import Model


class Manager(Model):
    """Админы и модераторы бота"""
    telegram_username = fields.CharField(max_length=255, unique=True)
    telegram_id = fields.BigIntField(unique=True, pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    role = fields.TextField(max_length=32, default=None,
                            null=True)  # роль усправленца

    class Meta:
        table = "manager"


class ManagementAction(Model):
    """Действия админов и модеров"""
    id = fields.IntField(pk=True)
    log_data = fields.CharField(max_length=512)
    owner = fields.ForeignKeyField(
        'models.Manager', related_name='man_log', on_delete=fields.CASCADE)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "manager_action"


class GlobalSettings(Model):
    allow_self_run = fields.BooleanField(default=True)
    enable_moderation = fields.BooleanField(default=True)

    message_interval_min = fields.IntField(default=3)
    message_interval_max = fields.IntField(default=6)
    loop_interval_min = fields.IntField(default=1800)
    loop_interval_max = fields.IntField(default=3600)
    message_limit = fields.IntField(default=75)

    class Meta:
        table = "settings"


class Channels(Model):
    """Список каналов со специфичными интервалами"""
    id = fields.IntField(pk=True)
    channel = fields.CharField(max_length=64, unique=True)
    timeout = fields.BigIntField(null=True, blank=True)  # интервал рассылки
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "all_channel"


class Notification(Model):
    id = fields.IntField(pk=True)
    data = fields.TextField(max_length=512)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "notification"


class StaticText(Model):
    """Текст приветствия для новых пользователей бота которые жмут '/start' """
    id = fields.IntField(pk=True)
    welcome = fields.TextField(default="Текст приветствия по кнопке /start")
    support = fields.TextField(
        default="Текст при нажатии на кнопку /Поддержка")
    rules = fields.TextField(default="Правила сервиса", null=True)

    class Meta:
        table = "static_text"
