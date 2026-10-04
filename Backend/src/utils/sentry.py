import sentry_sdk
from src.utils.settings import setting

def init_sentry():
    if not setting.SENTRY_DSN:
        return


    if setting.FASTAPI_ENV == "PRODUCTION":
        sentry_sdk.init(
            dsn=setting.SENTRY_DSN,
            environment=setting.FASTAPI_ENV,
            traces_sample_rate=0.1, # only monitor 10% of total data
            send_default_pii=False # sentry not capture sensitive data from query
        )


