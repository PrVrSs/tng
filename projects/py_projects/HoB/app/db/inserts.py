from datetime import date
from app.db.tables.worker import Worker
from app.db.db_connector import DBConnector


connector = DBConnector()

session = connector.session()

worker_1 = Worker("Matt Damon", date(1972, 5, 2))
worker_2 = Worker("Dwayne Johnson", date(1972, 5, 2))
worker_3 = Worker("Mark Wahlberg", date(1971, 6, 5))

session.add(worker_1)
session.add(worker_2)
session.add(worker_3)

session.commit()
