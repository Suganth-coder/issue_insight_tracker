import os

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from library.error_handling import ErrorHandling

class DataBase:

    def __init__(self, table_name, schema):
        url = URL.create(
            drivername=os.getenv("DB_DRIVER"),
            username=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_CONNECTIOT_NAME"),
            port=os.getenv("DB_PORT")
        )

        self.engine = create_engine(url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.check_connection()
        self.__init_db(table_name, schema)

    def __init_db(self, table_name, schema):
        """
        * Checks the database for table table_name
        * If it does not exist, create the table with given schema, else do nothing
        @return: 200 | 500
        """
        result = inspect(self.engine)
        if not result.has_table(table_name):
            print(f"Table {table_name} not found. Creating tables...")

            if schema is None:
                raise ValueError("Schema must be provided to create tables.")
            
            schema.metadata.create_all(self.engine)
            print("Tables created successfully.")
        else:
            print(f"Table {table_name} already exists.")

        return 200

    def check_connection(self):
        """
        Check if the database connection is successful.
        @return: NONE
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                print("Connection successful:", result.scalar() == 1)
        except Exception as e:
            print("Connection failed:", e)


    def get_session(self):
        return self.session
    