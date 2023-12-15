from schemas.common.response import Response_Validation_List_Schema
from schemas.common.exception import Exception_Schema

errors = {
    400: {"model": Exception_Schema},
    404: {"model": Exception_Schema},
    422: {"model": Response_Validation_List_Schema},
}
