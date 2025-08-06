from Parameters import *
from pydantic import BaseModel


class Settings(BaseModel):
    host: str
    port: str
    user: str
    password: str
    db_name: str

    def CREATE_SYNC_ENGINE(self):
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"

    def CREATE_ASYNC_ENGINE(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


settings = Settings(host=host, port=port, user=user, password=password, db_name=db_name)
