from pydantic import BaseSettings

class Settings(BaseSettings):
    #HERE LIES A CONFIG TO ALL SERVICE RELATED STUFF

    #AIOGRAM BOT
    BOT_TOKEN: str

    #LOGS
    LOG_PATH: str = "./Logs/"
    LOG_LEVEL: str = "INFO"
    LOG_ROTATION: str = "1 MB"
    LOG_RETENTION: str = "1 day"

    #BROKER
    BROKER_URL: str
    BROKER_SEARCH_QUERY_IN_TOPIC: str
    BROKER_SEARCH_QUERY_OUT_TOPIC: str
    BROKER_ADD_DOCUMENT_TOPIC: str


    class Config:
        env_file = ".env"

def get_settings() -> Settings:
    return Settings()
