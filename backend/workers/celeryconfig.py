from decouple import config
from kombu import Queue

DATABASE_URL = str(config("DATABASE_URL"))
BROKER_URL = str(config("BROKER_URL"))

broker_url = BROKER_URL
result_backend = f'db+{DATABASE_URL}'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
enable_utc = True
task_track_started = True

correcao_problema_queue = Queue("correcao-problema")
task_queues = (correcao_problema_queue,)
