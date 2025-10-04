from fastapi import HTTPException, status


class DefaultException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class InvalidRssLink(DefaultException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Ссылка неявляется rss"


class RssLinkAlreadyExist(DefaultException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    detail = "Ссылка уже отслеживается"


class FeedNotFound(DefaultException):
    status_code = status.HTTP_204_NO_CONTENT
    detail = "Новостная лента не существует"


class RssLinkAlreadyFollow(DefaultException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Вы уже отслеживаете эту ссылку"


class UserAlreadyExistsException(DefaultException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(DefaultException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenJwtException(DefaultException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен не представлен в виде JWT"


class TokenAbsentException(DefaultException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectIdType(DefaultException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Айди пользователя неправильного типа"


class IncorrectId(DefaultException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователя не существует"


class IncorrectRole(DefaultException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Вы не являетесь администратором"


class UserAlreadyLogin(DefaultException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Вы уже вошли"
