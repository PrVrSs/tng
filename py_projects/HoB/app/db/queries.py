from app.db.tables.worker import Worker
from app.db.db_connector import DBConnector


connector = DBConnector()

workers = connector.read_item(Worker)

for worker in workers:
    print(f'{worker.id} - {worker.name}')
