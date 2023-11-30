<section align="center" style="margin-bottom: 2em">
    <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/alcides07" width="200px;" alt="Autor 1"/>
  <h4>API em desenvolvimento</h4>
  <div>
    <a href="#tecnologias-utilizadas">Tecnologias</a> •
    <a href="#execução-do-projeto">Execução</a> 
  </div>
</section>

## Tecnologias utilizadas

> As seguintes tecnologias foram utilizadas no desenvolvimento do backend projeto:

-   [FastAPI 0.104.1](https://fastapi.tiangolo.com/)
-   [SQLAlchemy 2.0.23](https://www.sqlalchemy.org/)
-   [PostgreSQL 14.9](https://www.postgresql.org/)
-   [Docker Compose](https://docs.docker.com/compose/)

## Execução do projeto

### Ferramentas necessárias

> Para executar o projeto, você precisa ter instalado em sua máquina as seguintes ferramentas:

-   [Git](https://git-scm.com)
-   [Docker](https://docs.docker.com/get-docker/)
-   [Python 3.10](https://www.python.org/downloads/)

> Após a instalação de todas as ferramentas acima, prossiga:

### Clone o repositório:

```
git clone https://github.com/alcides07/Juiz-Online.git
```

### Acesse o diretório gerado:

```
cd Juiz-Online/backend/
```

### Crie um ambiente virtual:

```
python3 -m venv venv
```

### Ative o ambiente virtual (Linux):

```
. venv/bin/activate
```

### Ative o ambiente virtual (Windows):

```
.\venv\Scripts\activate
```

### Execute com Docker Compose:

```
docker-compose up --build
```

### Executando com Uvicorn

### Instale as dependências:

```
pip install -r requirements.txt
```

### Execute a aplicação:

```
uvicorn main:app --reload
```
