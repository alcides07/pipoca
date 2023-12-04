<section align="center" style="margin-bottom: 2em">
    <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/alcides07" width="200px;" alt="Desenvolvedor Alcides Dantas"/>
  <h4>API em desenvolvimento</h4>
  <div>
    <a href="#tecnologias-utilizadas">Tecnologias</a> •
    <a href="#execução-do-projeto">Execução</a> 
  </div>
</section>

## 1. Tecnologias utilizadas

> As seguintes tecnologias foram utilizadas no desenvolvimento do backend projeto:

-   [FastAPI 0.104.1](https://fastapi.tiangolo.com/)
-   [Uvicorn 0.23.2](https://www.uvicorn.org/)
-   [SQLAlchemy 2.0.23](https://www.sqlalchemy.org/)
-   [PostgreSQL 14.9](https://www.postgresql.org/)
-   [Docker Compose 1.29.2](https://docs.docker.com/compose/)

## 2. Execução do projeto

### 2.1. Ferramentas necessárias

> Para executar o projeto, você precisa possuir previamente em sua máquina as seguintes ferramentas:

-   [Git](https://git-scm.com)
-   [Docker 24.0.5](https://docs.docker.com/get-docker/)
-   [Python 3.10](https://www.python.org/downloads/)
-   [Docker Compose 1.29.2](https://docs.docker.com/compose/)

<details>
  <summary><h3>2.2. Execução com Uvicorn:</h3></summary>

#### 2.2.1. Clone o repositório:

```
git clone https://github.com/alcides07/Juiz-Online.git
```

#### 2.2.2. Acesse o diretório gerado:

```
cd Juiz-Online/backend/
```

#### 2.2.3. Crie um ambiente virtual:

```
python3 -m venv venv
```

#### 2.2.4. Ative o ambiente virtual (Linux):

```
. venv/bin/activate
```

Ou

#### 2.2.4. Ative o ambiente virtual (Windows):

```
.\venv\Scripts\activate
```

#### 2.2.5. Instale as dependências:

```
pip install -r requirements.txt
```

#### 2.2.6. Execute a aplicação:

```
uvicorn main:app --reload
```

</details>

<details>
  <summary><h3>2.3. Execução com Docker Compose:</h3></summary>

#### 2.3.1. Clone o repositório:

```
git clone https://github.com/alcides07/Juiz-Online.git
```

#### 2.3.2. Acesse o diretório gerado:

```
cd Juiz-Online/backend/
```

#### 2.3.3. Execute a aplicação:

```
docker-compose up --build
```

</details>
