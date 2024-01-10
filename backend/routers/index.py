from routers import arquivo, openapi, user, problema, auth


routes = [
    openapi.router,
    user.router,
    problema.router,
    auth.router,
    arquivo.router,
]
