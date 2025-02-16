from backend.src.services.angel_broker import AngelBroker
from backend.src.core.logger import setup_logger

logger = setup_logger(__name__)

def main():
    broker = AngelBroker()
    session = None
    logger.info("Starting trading application", extra={
        'extra_fields': {
            'action': 'application_start',
            'version': '1.0.0'
        }
    })

    try:
        session = broker.login()
        logger.info("Login successful!", extra={
            'extra_fields': {
                'session_active': True,
                'action': 'login_complete'
            }
        })

        while True:
            logger.debug("Displaying menu to user", extra={
                'extra_fields': {
                    'action': 'show_menu',
                    'session_active': bool(session)
                }
            })
            
            print("\n1. Check connection")
            print("2. Exit")
            cmd = input("\nChoice: ")
            
            logger.info("User input received", extra={
                'extra_fields': {
                    'action': 'user_input',
                    'choice': cmd
                }
            })

            if cmd == "1":
                connection_status = bool(session and session.token)
                logger.info("Connection status checked", extra={
                    'extra_fields': {
                        'action': 'check_connection',
                        'status': 'connected' if connection_status else 'disconnected',
                        'has_session': bool(session),
                        'has_token': bool(session and session.token)
                    }
                })
                print(f"Status: {'Connected' if connection_status else 'Not connected'}")
            
            elif cmd == "2":
                logger.info("User requested exit", extra={
                    'extra_fields': {
                        'action': 'exit_requested',
                        'session_active': bool(session)
                    }
                })
                break
            else:
                logger.warning("Invalid choice entered", extra={
                    'extra_fields': {
                        'action': 'invalid_input',
                        'input': cmd
                    }
                })
                print("Invalid choice")

    except KeyboardInterrupt:
        logger.info("Application interrupted by user", extra={
            'extra_fields': {
                'action': 'keyboard_interrupt',
                'session_active': bool(session)
            }
        })
    except Exception as e:
        logger.error(f"Application error: {str(e)}", extra={
            'extra_fields': {
                'action': 'application_error',
                'error_type': type(e).__name__,
                'error_details': str(e)
            }
        })
    finally:
        if session:
            try:
                broker.logout(session)
                logger.info("Application shutdown complete", extra={
                    'extra_fields': {
                        'action': 'application_shutdown',
                        'status': 'clean'
                    }
                })
            except Exception as e:
                logger.error(f"Logout failed: {str(e)}", extra={
                    'extra_fields': {
                        'action': 'logout_error',
                        'error_type': type(e).__name__,
                        'error_details': str(e)
                    }
                })
