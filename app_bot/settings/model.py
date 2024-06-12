from pydantic import BaseModel, SecretStr, fields
from pydantic_settings import SettingsConfigDict


class BotSettings(BaseModel):
    bot_token: SecretStr = fields.Field(max_length=100, alias='TELEGRAM_BOT_TOKEN')
    bot_link: str = fields.Field(max_length=100, alias='BOT_BASE_LINK')
    admin_password: SecretStr = fields.Field(max_length=100, alias='ADMIN_PASSWORD')
    required_channel_id: str = fields.Field(alias='REQUIRED_CHANNEL_ID')
    currency_chat_id: int = fields.Field(alias='CURRENCY_CHAT_ID')
    deep_link_args: str = fields.Field(max_length=100, alias='DEEP_LINK_ARGS')


class StaticContent(BaseModel):
    welcome_post_id: int = fields.Field(alias='welcome_post_id'.upper())
    info_post_id: int = fields.Field(alias='info_post_id'.upper())
    socials_post_id: int = fields.Field(alias='socials_post_id'.upper())
    addresses_post_id: int = fields.Field(alias='addresses_post_id'.upper())
    payment_data_post_id: int = fields.Field(alias='payment_data_post_id'.upper())
    delivery_post_id: int = fields.Field(alias='delivery_post_id'.upper())
    requirements_post_id: int = fields.Field(alias='requirements_post_id'.upper())
    poizon_post_id: int = fields.Field(alias='poizon_post_id'.upper())
    alipay_post_id: int = fields.Field(alias='alipay_post_id'.upper())
    contract_post_id: int = fields.Field(alias='contract_post_id'.upper())
    cases_post_id: int = fields.Field(alias='cases_post_id'.upper())
    reviews_post_id: int = fields.Field(alias='reviews_post_id'.upper())
    currency_post_id: int = fields.Field(alias='currency_post_id'.upper())

    notification_post_id: int = fields.Field(alias='NOTIFICATION_POST_ID')
    registered_post_id: int = fields.Field(alias='REGISTERED_POST_ID')


class Dialogues(BaseModel):
    categories_per_page_height: int = fields.Field(alias='CATEGORIES_HEIGHT')
    categories_per_page_width: int = fields.Field(alias='CATEGORIES_WIDTH')
    faq_per_page_height: int = fields.Field(alias='FAQ_HEIGHT')
    faq_per_page_width: int = fields.Field(alias='FAQ_WIDTH')


class Broadcaster(BaseModel):
    mailing_batch_size: int = fields.Field(alias='MAILING_BATCH_SIZE', default=25)
    broadcaster_sleep: int = fields.Field(alias='BROADCASTER_SLEEP', default=1)
    notification_hours: int = fields.Field(alias='NOTIFICATION_HOURS', default=10)
    notification_minutes: int = fields.Field(alias='NOTIFICATION_MINUTES', default=0)
    notification_hours_1: int = fields.Field(alias='NOTIFICATION_HOURS_1', default=9)
    notification_hours_3: int = fields.Field(alias='NOTIFICATION_HOURS_2', default=15)
    notification_hours_2: int = fields.Field(alias='NOTIFICATION_HOURS_3', default=21)


class AppSettings(BaseModel):
    prod_mode: bool = fields.Field(alias='PROD_MODE', default=False)
    excel_file: str = fields.Field(alias='EXCEL_FILE', default='Users stats.xlsx')


class PostgresSettings(BaseModel):
    db_user: str = fields.Field(alias='POSTGRES_USER')
    db_host: str = fields.Field(alias='POSTGRES_HOST')
    db_port: int = fields.Field(alias='POSTGRES_PORT')
    db_pass: SecretStr = fields.Field(alias='POSTGRES_PASSWORD')
    db_name: SecretStr = fields.Field(alias='POSTGRES_DATABASE')


class RedisSettings(BaseModel):
    redis_host: str = fields.Field(alias='REDIS_HOST')
    redis_port: int = fields.Field(alias='REDIS_PORT')
    redis_name: str = fields.Field(alias='REDIS_NAME')


class Settings(
    BotSettings,
    StaticContent,
    AppSettings,
    PostgresSettings,
    Broadcaster,
    Dialogues,
    RedisSettings
):
    model_config = SettingsConfigDict(extra='ignore')
