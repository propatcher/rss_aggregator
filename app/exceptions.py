from fastapi import HTTPException, status


class DefaultException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class IncorrectEmailOrPasswordException(DefaultException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"
