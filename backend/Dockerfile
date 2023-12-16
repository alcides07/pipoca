FROM python:3.10
RUN groupadd -r group && useradd -r -g group user
WORKDIR /API
RUN chown -R user:group /API
COPY requirements.txt . 
RUN pip install -r requirements.txt
COPY . .
USER user