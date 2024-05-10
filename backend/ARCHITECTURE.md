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

│   ├── orm                             # Métodos de manipulação de banco de dados

│       ├── common                      # Métodos genéricos que são reaproveitados

│   ├── routers                         # Rotas da API

│       ├── common                      

│           ├── index.py                # Barril de exportação de rotas

│   ├── schemas                         # Classes de validação de modelos

│       ├── common                      # Classes globais que são reaproveitadas

│   ├── tests                           # Diferentes tipos de testes da aplicação

│       ├── helpers                     # Métodos de ajuda que são reaproveitados em diversos testes

│       ├── integration                 # Testes de integração

│       ├── unit                        # Testes unitários

│       ├── config_teste.py             # Configuração de ambiente de testes

│       ├── database.py                 # Configuração de banco de dados de teste

│   ├── utils                       # Métodos utilitários que são reaproveitados

│   ├── Dockerfile.koyeb            # Dockerfile exclusivo para ativar o Daemon Docker no Koyeb

│   ├── compilers.py                # Comandos para compilar e executar códigos em diferentes linguagens

│   ├── constants.py                # Constantes globais da aplicação

│   ├── database.py                 # Configuração de banco de dados principal

│   ├── main.py                     # Arquivo de inicialização da aplicação

│   ├── sonar-project.properties    # Propriedades do projeto da ferramenta Sonar

│   ├── tox.ini                     # Configuração da ferramenta Tox para execução de testes

└── ...
```