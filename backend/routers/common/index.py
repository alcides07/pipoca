from routers import arquivo, auth, declaracao, openapi, problema, problemaTeste, tag, user, validador, validadorTeste, verificador, verificadorTeste

routes = [
    arquivo.router,
    auth.router,
    declaracao.router,
    openapi.router,
    problema.router,
    problemaTeste.router,
    tag.router,
    user.router,
    validador.router,
    validadorTeste.router,
    verificador.router,
    verificadorTeste.router
]
