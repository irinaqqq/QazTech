import psycopg2
from psycopg2 import OperationalError

try:
    cnx = psycopg2.connect(
        user="useradmin",  # Обрати внимание: в Azure обычно user с @hostname
        password="foZtox-simmyf-ryxni9",
        host="database-postgres-test.postgres.database.azure.com",
        port=5432,
        database="my_test_db",
    )
    print("Connection successful")
    cnx.close()
except OperationalError as e:
    print("Error connecting to PostgreSQL:", e)
