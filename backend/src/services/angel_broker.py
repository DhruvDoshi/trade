import pyotp
import requests
from dataclasses import dataclass
from backend.src.config.credentials import get_credentials
from backend.src.config.api_endpoints import AngelOneAPI
from backend.src.core.logger import setup_logger

logger = setup_logger(__name__)

@dataclass
class BrokerSession:
    token: str
    client: requests.Session

class AngelBroker:
    def __init__(self):
        self.credentials = get_credentials()
        self.timeout = 10
        self.logger = setup_logger(__name__)

    def _headers(self, token=None):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-UserType': 'USER',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': self.credentials.CLIENT_LOCAL_IP,
            'X-ClientPublicIP': self.credentials.CLIENT_PUBLIC_IP,
            'X-MACAddress': self.credentials.MAC_ADDRESS,
            'X-PrivateKey': self.credentials.API_KEY
        }
        if token:
            headers['Authorization'] = f"Bearer {token}"
        return headers

    def login(self) -> BrokerSession:
        try:
            self.logger.info("Initiating login", extra={
                'extra_fields': {
                    'username': self.credentials.USERNAME,
                    'client_ip': self.credentials.CLIENT_PUBLIC_IP,
                    'action': 'login_attempt'
                }
            })
            
            session = requests.Session()
            totp = pyotp.TOTP(self.credentials.TOTP_SECRET).now()
            
            response = session.post(
                AngelOneAPI.LOGIN,
                json={
                    "clientcode": self.credentials.USERNAME,
                    "password": self.credentials.MPIN,
                    "totp": totp,
                    "state": "state"
                },
                headers=self._headers(),
                timeout=self.timeout
            ).json()

            if not response.get('status'):
                self.logger.error("Login failed", extra={
                    'extra_fields': {
                        'error': response.get('message'),
                        'status_code': response.get('status'),
                        'username': self.credentials.USERNAME,
                        'action': 'login_failed'
                    }
                })
                raise Exception(response.get('message', 'Login failed'))

            self.logger.info("Login successful", extra={
                'extra_fields': {
                    'username': self.credentials.USERNAME,
                    'session_id': session.cookies.get('session_id'),
                    'action': 'login_success'
                }
            })

            return BrokerSession(
                token=response['data']['jwtToken'],
                client=session
            )

        except Exception as e:
            self.logger.error("Login error", extra={
                'extra_fields': {
                    'error_type': type(e).__name__,
                    'error_message': str(e),
                    'username': self.credentials.USERNAME,
                    'action': 'login_error'
                }
            })
            raise

    def logout(self, session: BrokerSession):
        try:
            self.logger.info("Initiating logout", extra={
                'extra_fields': {
                    'username': self.credentials.USERNAME,
                    'action': 'logout_attempt'
                }
            })
            
            response = session.client.post(
                AngelOneAPI.LOGOUT,
                json={"clientcode": self.credentials.USERNAME},
                headers=self._headers(session.token),
                timeout=self.timeout
            ).json()

            if not response.get('status'):
                self.logger.error("Logout failed", extra={
                    'extra_fields': {
                        'error': response.get('message'),
                        'username': self.credentials.USERNAME,
                        'action': 'logout_failed'
                    }
                })
                raise Exception(response.get('message', 'Logout failed'))
            
            self.logger.info("Logout successful", extra={
                'extra_fields': {
                    'username': self.credentials.USERNAME,
                    'action': 'logout_success'
                }
            })

        except Exception as e:
            self.logger.error("Logout error", extra={
                'extra_fields': {
                    'error_type': type(e).__name__,
                    'error_message': str(e),
                    'username': self.credentials.USERNAME,
                    'action': 'logout_error'
                }
            })
            raise
