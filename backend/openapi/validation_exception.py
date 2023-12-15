from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import status, Request
from utils.translate import translate
from schemas.common.response import Response_Validation_List_Schema, Response_Validation_Schema


def validation_exception_handler(request: Request, exception: RequestValidationError):
    response = Response_Validation_List_Schema(
        errors=[
            Response_Validation_Schema(
                field=error["loc"][1],
                type=error["type"],
                message=translate(text=error["msg"])
            )
            for error in exception.errors()
        ]
    )

    return JSONResponse(
        content=jsonable_encoder(response),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
