from schemas.common.pagination import pagination_schema


async def pagination_router(q: str = "", skip: int = None, limit: int = None):
    return pagination_schema(q=q, skip=skip, limit=limit)
