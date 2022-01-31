from tortoise import fields
from tortoise.models import Model


class Post(Model):
    """Рекламный пост клиента"""
    id = fields.IntField(pk=True)
    owner = fields.ForeignKeyField(
        'models.Client', related_name='post_owner', on_delete=fields.CASCADE)
    photo = fields.CharField(max_length=255, default=None, null=True)
    message = fields.TextField(default="Текст рекламы", max_length=4096)
    reply_text = fields.TextField(default="Текст рекламы")
    category = fields.CharField(default="базовая", max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    status = fields.BooleanField(default=False)
    # интервалы сообщений
    use_message_interval = fields.BooleanField(
        default=False)  # использовать глобальный интервал
    message_interval_min = fields.IntField(default=3)
    message_interval_max = fields.IntField(default=6)
    loop_interval_min = fields.IntField(default=1800)
    loop_interval_max = fields.IntField(default=3600)

    #  премодерация
    m_message = fields.TextField(default=None, null=True)
    m_reply_text = fields.TextField(default=None, null=True)
    m_photo = fields.CharField(max_length=255, default=None, null=True)
    #  Использовать кастомные данные сессии
    user_custom_info = fields.BooleanField(default=True)
    custom_name = fields.CharField(max_length=32, null=True, default=None)
    custom_surname = fields.CharField(max_length=32, null=True, default=None)
    custom_photo = fields.CharField(max_length=256, null=True, default=None)
    custom_status = fields.CharField(max_length=70, null=True, default=None)

    m_status = fields.BooleanField(default=False)
    current_session = fields.OneToOneField(
        "models.Session", null=True, default=None)

    class Meta:
        table = "post"


class SendLog(Model):
    """Логи рассылки для конкретного объявления"""
    id = fields.IntField(pk=True)
    post = fields.ForeignKeyField(
        'models.Post', related_name='post_logs', on_delete=fields.CASCADE)
    link = fields.CharField(default=None, max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "send_log"


class IncomeMessage(Model):
    id = fields.IntField(pk=True)
    from_user = fields.TextField(max_length=64)
    message = fields.TextField(max_length=4096)
    created_at = fields.DatetimeField(auto_now_add=True)
    to_post = fields.ForeignKeyField(
        'models.Post', related_name='post_income_message', on_delete=fields.CASCADE)

    class Meta:
        table = "income_message"
