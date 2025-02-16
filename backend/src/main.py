from backend.src.services.auth import AuthService
from backend.src.core.logger import setup_logger

logger = setup_logger(__name__)

def main():
    auth = AuthService()
    session = None

    try:
        session = auth.login()
        logger.info("Login successful!")

        while True:
            cmd = input("\n1. Check status\n2. Exit\nChoice: ")
            if cmd == "1":
                print("Connected!")
            elif cmd == "2":
                break

    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        if session:
            try:
                auth.logout(session)
                logger.info("Logged out successfully")
            except Exception as e:
                logger.error(f"Logout failed: {e}")
