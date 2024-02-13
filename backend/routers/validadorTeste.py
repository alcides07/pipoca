from dependencies.authenticated_user import get_authenticated_user
from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(
    prefix="/validadorTestes",
    tags=["validadorTeste"],
    dependencies=[Depends(get_authenticated_user)],
    deprecated=True
)


@router.get("/")
async def read(
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.get("/{id}/")
async def read_id(
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.post("/")
async def create(
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.patch("/{id}/")
async def parcial_update(
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.put("/{id}/")
async def total_update(
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.delete("/{id}/")
async def delete(
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
