<!-- prettier-ignore-start -->

# Estrutura do projeto
 
A maior parte do projeto reside no diretório `src` e pode ser visualizada abaixo:
```
├── frontend

│   ├── node_modules                    # Dependências do projeto

│   ├── src                             # Códigos-fonte da aplicação

│       ├── assets                      # Arquivos estáticos como imagens, fontes etc.

│       ├── components                  # Componentes globais da aplicação

│           ├── componentExample        # Exemplo de componente espefícico para esta aplicação

│           ├── ui                      # Componentes da coleção de componentes reutilizáveis Shadcn/ui

│       ├── features                    # Funcionalidades da aplicação

│           ├── moduleExample           # Agrupamento de funcionalidades similares e/ou equivalentes

│               ├── featureExample      # Funcionalidade específica

│                   ├── components      # Componentes específicos de uma funcionalidade

│                   ├── index.tsx       # Página central de uma funcionalidade

│       ├── interfaces                  # Definição das interfaces da aplicação

│           ├── models                  # Interfaces de entidades a fim de popular os componentes

│           ├── services                # Interfaces de entidades a fim de lidar com comunicações com a API

│       ├── lib                         # Bibliotecas de código ou funções utilitárias usadas em várias partes do projeto

│       ├── pages                       # Páginas globais da aplicação: telas de erro, configurações etc.

│       ├── routes                      # Definição e configuração do roteamento da aplicação

│       ├── services                    # Serviços externos utilizados pela aplicação

│               ├── axiosInstance.ts    # Configurações comuns a todos os serviços como headers, interceptors etc.
                
│               ├── models              # Serviço e endereço da API de cada entidade

│       ├── utils                       # Utilitários e funções auxiliares

└── ...
```
<!-- prettier-ignore-end -->
