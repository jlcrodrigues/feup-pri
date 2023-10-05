import database

db = database.Database("localhost", 5432, "pri", "pri", "pri23")
db.connect()
db.exec_file("schema.sql")
db.disconnect()