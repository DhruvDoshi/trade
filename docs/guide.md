# Angel One Trading Application Guide

## Overview
This application provides a Python-based interface for interacting with Angel One's trading API. It handles authentication, session management, and basic trading operations.

## Project Structure
```
/workspaces/trade/
├── backend/
│   └── src/
│       ├── config/
│       │   ├── api_endpoints.py  # API URLs and endpoints
│       │   └── credentials.py    # Broker credentials
│       ├── core/           
│       │   └── logger.py        # JSON logging
│       ├── services/
│       │   └── angel_broker.py  # Broker operations
│       └── main.py             # Application entry
├── docs/                      # Documentation
├── logs/                      # JSON logs
├── .env                       # Credentials
└── run.py                     # Entry point
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/DhruvDoshi/trade.git
   cd trade
   ```

2. **Environment Setup**
   Create a `.env` file in the root directory with your Angel One credentials:
   ```
   API_KEY=your_api_key
   USERNAME=your_username
   MPIN=your_mpin
   TOTP_SECRET=your_totp_secret
   CLIENT_LOCAL_IP=your_local_ip
   CLIENT_PUBLIC_IP=your_public_ip
   MAC_ADDRESS=your_mac_address
   DP_ID=your_dp_id
   BO_ID=your_bo_id
   PAN_CARD=your_pan_card
   ```

3. **Install Dependencies**
   ```bash
   make install
   ```

4. **Run the Application**
   ```bash
   make run
   ```

## Features

### Authentication
- Automatic TOTP generation
- Session management
- Secure credential handling

### Logging
- Console and file logging
- Logs stored in `/logs/trading.log`
- Detailed error tracking

## Code Components

### Broker Service (angel_broker.py)
- Manages Angel One broker operations
- Handles authentication and sessions
- Provides broker-specific functionality

### Credentials Management (credentials.py)
- Secure credential handling
- Environment configuration
- Broker-specific settings

### API Endpoints (api_endpoints.py)
- Angel One API endpoints
- API configuration
- Header definitions

### Logger (logger.py)
- Dual logging (console and file)
- Formatted log messages
- Debug information

## Usage Examples

1. **Basic Login and Status Check**
   ```python
   from backend.src.services.angel_broker import AngelBroker

   broker = AngelBroker()
   session = broker.login()
   # Perform operations
   broker.logout(session)
   ```

## Common Issues and Solutions

1. **TOTP Generation Fails**
   - Verify TOTP_SECRET in .env
   - Ensure correct time synchronization

2. **Connection Errors**
   - Check internet connectivity
   - Verify API endpoints
   - Confirm IP addresses in .env

3. **Authentication Fails**
   - Verify credentials in .env
   - Check API key status
   - Confirm MPIN is correct

## Development

### Adding New Features
1. Create new service in `/backend/src/services/`
2. Update main.py with new functionality
3. Add constants if needed
4. Update documentation

### Running Tests
```bash
make clean    # Clean cache files
make install  # Install dependencies
make run      # Run application
```

### Logs
- Application logs: `/logs/trading.log`
- Use `tail -f logs/trading.log` to monitor

## Security Notes
- Never commit .env file
- Keep TOTP_SECRET secure
- Regularly update credentials
- Monitor API usage

## Contributing
1. Fork the repository
2. Create feature branch
3. Submit pull request
4. Update documentation

## Support
For issues and support:
1. Check documentation
2. Review logs
3. Open GitHub issue
