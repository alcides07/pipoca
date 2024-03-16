from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import status
from utils.translate import translate
from schemas.common.response import ResponseValidationListSchema, ResponseValidationSchema


def validation_exception_handler(_, exception: RequestValidationError):
    response = ResponseValidationListSchema(
        errors=[
            ResponseValidationSchema(
                field=str(error["loc"][1]) if len(
                    error["loc"]) > 1 else "",
                type=translate(error["type"]),
                message=translate(text=error["msg"]),
            )
            for error in exception.errors()
        ]
    )

    return JSONResponse(
        content=jsonable_encoder(response),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
