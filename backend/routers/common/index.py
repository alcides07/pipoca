from routers import arquivo, openapi, user, problema, auth, validador, verificador


routes = [
    openapi.router,
    user.router,
    problema.router,
    auth.router,
    arquivo.router,
    verificador.router,
    validador.router,
]
