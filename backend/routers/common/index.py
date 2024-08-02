from routers import arquivo, auth, declaracao, openapi, problema, problemaResposta, problemaTeste, tag, user, validador, validadorTeste, verificador, verificadorTeste, tarefas

routes = [
    arquivo.router,
    auth.router,
    declaracao.router,
    openapi.router,
    problema.router,
    problemaResposta.router,
    problemaTeste.router,
    tag.router,
    user.router,
    validador.router,
    validadorTeste.router,
    verificador.router,
    verificadorTeste.router,
    tarefas.router
]
