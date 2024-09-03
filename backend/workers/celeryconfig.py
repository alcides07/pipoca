from kombu import Queue
from enviroments import BROKER_URL, DATABASE_URL, ENV


broker_url = BROKER_URL
result_backend = f'db+{DATABASE_URL}'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
enable_utc = True
task_track_started = True

correcao_problema_queue = Queue("correcao-problema")
importacao_problema_queue = Queue("importacao-problema")

task_queues = (correcao_problema_queue, importacao_problema_queue)


if (ENV == "test"):
    # Executa a tarefa de forma síncrona.
    task_always_eager = True
