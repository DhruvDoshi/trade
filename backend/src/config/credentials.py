from pathlib import Path
from pydantic import BaseSettings, Field
from functools import lru_cache
from backend.src.core.logger import setup_logger

logger = setup_logger(__name__)

class AngelOneCredentials(BaseSettings):
    API_KEY: str = Field(..., env='API_KEY')
    USERNAME: str = Field(..., env='USERNAME')
    MPIN: str = Field(..., env='MPIN')
    TOTP_SECRET: str = Field(..., env='TOTP_SECRET')
    CLIENT_LOCAL_IP: str = Field(..., env='CLIENT_LOCAL_IP')
    CLIENT_PUBLIC_IP: str = Field(..., env='CLIENT_PUBLIC_IP')
    MAC_ADDRESS: str = Field(..., env='MAC_ADDRESS')
    DP_ID: str = Field(..., env='DP_ID')
    BO_ID: str = Field(..., env='BO_ID')
    PAN_CARD: str = Field(..., env='PAN_CARD')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

@lru_cache()
def get_credentials() -> AngelOneCredentials:
    return AngelOneCredentials()
