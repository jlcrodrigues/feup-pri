import psycopg2

class Database:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    def connect(self):
        self.connection = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port = self.port
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.cursor.close()
        self.connection.close()

    def execute(self, query, params=None, fetch="all"):
        self.cursor.execute(query, params)
        self.connection.commit()
        
        try:
            match fetch:
                case "all":
                    return self.cursor.fetchall()
                case "one":
                    return self.cursor.fetchone()
                case "many":
                    return self.cursor.fetchmany()
                case _:
                    return None
        except Exception as e:
            self.connection.rollback()
            raise e
            
    def exec_file(self, file):
        with open(file, 'r') as f:
            self.cursor.execute(f.read())
            self.connection.commit()
    