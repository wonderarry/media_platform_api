from pydantic import BaseSettings



class Settings(BaseSettings):
    db_host : str 
    db_port : str 
    db_user : str 
    db_name : str 
    db_password : str 
    secretkey : str 
    algorithm : str 
    access_token_expire_minutes : int

    class Config:
        env_file = '.env'

settings = Settings()
print(settings.db_host)