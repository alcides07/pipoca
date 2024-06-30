# Estrutura do projeto

```
├── backend

│   ├── dependencies                    # Funções de dependências globais

│   ├── filters                         # Classes de filtros para as rotas da API

│   ├── migrations                      # Migrações de banco de dados

│       ├── env.py                      # Configurações das migrações


│   ├── models                          # Entidades da aplicação

│       ├── common

│           ├── index.py                # Barril de exportação de entidades

│   ├── openapi                         # Configurações adicionais do openapi

│   ├── orm                             # Funções de manipulação de banco de dados

│       ├── common                      # Funções genéricas que podem ser reaproveitados

│   ├── routers                         # Rotas da API

│       ├── common

│           ├── index.py                # Barril de exportação de rotas

│   ├── schemas                         # Classes de validação de modelos

│       ├── common                      # Classes globais que são reaproveitadas

│   ├── tests                           # Diferentes tipos de testes

│       ├── helpers                     # Funções auxiliares para construção dos testes

│       ├── integration                 # Testes de integração

│       ├── unit                        # Testes unitários

│       ├── config_teste.py             # Configuração de ambiente de testes

│       ├── database.py                 # Configuração de banco de dados de teste

│   ├── utils                       # Funções utilitárias globais

│   ├── Dockerfile.koyeb            # Dockerfile exclusivo para ativar o Daemon Docker no Koyeb

│   ├── compilers.py                # Comandos de compilação e execução de códigos em diferentes linguagens

│   ├── constants.py                # Constantes globais da aplicação

│   ├── database.py                 # Configuração de banco de dados principal

│   ├── main.py                     # Arquivo de inicialização da aplicação

│   ├── sonar-project.properties    # Propriedades do projeto na ferramenta Sonar

│   ├── tox.ini                     # Configuração da ferramenta Tox para execução de testes

└── ...
```
