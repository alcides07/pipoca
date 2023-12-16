from schemas.common.response import ResponseValidationListSchema
from schemas.common.exception import ExceptionSchema

errors = {
    400: {"model": ExceptionSchema},
    401: {"model": ExceptionSchema},
    404: {"model": ExceptionSchema},
    422: {"model": ResponseValidationListSchema},
}
