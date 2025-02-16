class API:
    BASE_URL = "https://apiconnect.angelone.in/rest"
    LOGIN = f"{BASE_URL}/auth/angelbroking/user/v1/loginByPassword"
    LOGOUT = f"{BASE_URL}/secure/angelbroking/user/v1/logout"

class APIHeaders:
    CONTENT_TYPE = "application/json"
    USER_TYPE = "USER"
    SOURCE_ID = "WEB"
