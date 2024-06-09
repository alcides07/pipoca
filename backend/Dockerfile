FROM python:3.10

RUN groupadd -r group && useradd -r -g group user
WORKDIR /API
RUN chown -R user:group /API

COPY requirements.txt . 
RUN pip install -r requirements.txt

COPY ./dependencies ./dependencies
COPY ./models ./models
COPY ./openapi ./openapi
COPY ./migrations ./migrations
COPY ./orm ./orm
COPY ./routers ./routers
COPY ./schemas ./schemas
COPY ./tests ./tests
COPY ./utils ./utils
COPY ./filters ./filters
COPY ./static ./static
COPY database.py .
COPY compilers.py .
COPY constants.py .
COPY main.py .
COPY alembic.ini .
COPY enviroments.py .

# USER user