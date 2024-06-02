from .controller import route_base
from fastapi import Request, status
from fastapi.responses import JSONResponse


class UserNotFound(Exception):
    def __init__(self, msg: str) -> None:
        self.name = msg


@route_base.exception_handler(UserNotFound)
async def user_not_found_exception(reqeust: Request, exception: UserNotFound):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": f"Eror: {exception.name}, please check and try again.",
            "trace": exception.with_traceback(),
        },
    )


class PasswordValidationException(Exception):
    def __init__(self, msg: str) -> None:
        self.name = msg


@route_base.exception_handler(PasswordValidationException)
async def user_not_found_exception(
    reqeust: Request, exception: PasswordValidationException
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": f"Eror: {exception.name}, please check and try again.",
            "trace": exception.with_traceback(),
        },
    )
