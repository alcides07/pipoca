from routers import openapi, user, problema, auth


routes = [
    openapi.router,
    user.router,
    problema.router,
    auth.router,
]
