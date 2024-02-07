from fastapi import APIRouter, HTTPException, status


router = APIRouter(
    prefix="/respostas",
    tags=["resposta"],
    deprecated=True,
)


@router.get("/")
async def read(
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
