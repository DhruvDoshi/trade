import pyotp
import requests
from dataclasses import dataclass
from backend.src.config.settings import get_settings
from backend.src.config.constants import API
from backend.src.core.logger import setup_logger

logger = setup_logger(__name__)

@dataclass
class Session:
    token: str
    client: requests.Session

class AuthService:  # Note: Changed from Auth to AuthService
    def __init__(self):
        self.settings = get_settings()
        self.timeout = 10

    def _headers(self, token=None):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-UserType': 'USER',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': self.settings.CLIENT_LOCAL_IP,
            'X-ClientPublicIP': self.settings.CLIENT_PUBLIC_IP,
            'X-MACAddress': self.settings.MAC_ADDRESS,
            'X-PrivateKey': self.settings.API_KEY
        }
        if token:
            headers['Authorization'] = f"Bearer {token}"
        return headers

    def login(self) -> Session:
        try:
            session = requests.Session()
            totp = pyotp.TOTP(self.settings.TOTP_SECRET).now()
            
            response = session.post(
                API.LOGIN,
                json={
                    "clientcode": self.settings.USERNAME,
                    "password": self.settings.MPIN,
                    "totp": totp,
                    "state": "state"
                },
                headers=self._headers(),
                timeout=self.timeout
            ).json()

            if not response.get('status'):
                raise Exception(response.get('message', 'Login failed'))

            return Session(
                token=response['data']['jwtToken'],
                client=session
            )

        except Exception as e:
            logger.error(f"Login failed: {e}")
            raise

    def logout(self, session: Session):
        try:
            response = session.client.post(
                API.LOGOUT,
                json={"clientcode": self.settings.USERNAME},
                headers=self._headers(session.token),
                timeout=self.timeout
            ).json()

            if not response.get('status'):
                raise Exception(response.get('message', 'Logout failed'))
            
            logger.info("Logout successful")

        except Exception as e:
            logger.error(f"Logout failed: {e}")
            raise
