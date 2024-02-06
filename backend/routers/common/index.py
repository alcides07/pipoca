from routers import arquivo, openapi, user, problema, auth, validador, verificador


routes = [
    arquivo.router,
    auth.router,
    openapi.router,
    problema.router,
    user.router,
    validador.router,
    verificador.router
]
