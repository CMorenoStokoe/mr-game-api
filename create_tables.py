import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

insert_query = "INSERT INTO users VALUES (NULL, ?, ?)"

users = [
	('chris', 'pass'),
	('user1', 'password'),
	('admin', 'authorised')
]
cursor.executemany(insert_query, users)

create_table = "CREATE TABLE IF NOT EXISTS edges (ref INTEGER PRIMARY KEY, exposure int, exp_name text, outcome int, out_name text, MRestimate real)"
cursor.execute(create_table)

insert_query = "INSERT INTO edges VALUES (NULL, ?, ?, ?, ?, ?)"

edges = [
	(1, 'Adiponectin', 10, 'CrohnsDisease', 0.001),
	(1, 'Adiponectin', 100, 'HipCircumfrance', 0.002),
	(1, 'Adiponectin', 1000, 'DepressiveSymptoms', 0.003),
	(10, 'CrohnsDisease', 100, 'HipCircumfrance', 0.004),
	(10, 'CrohnsDisease', 1000, 'DepressiveSymptoms', 0.005),
	(100, 'HipCircumfrance', 1000, 'DepressiveSymptoms', 0.006)	
]
cursor.executemany(insert_query, edges)

create_table = "CREATE TABLE IF NOT EXISTS annotations (annotID INTEGER PRIMARY KEY, ref int, username text, judgement int, comment text)"
cursor.execute(create_table)

insert_query = "INSERT INTO annotations VALUES (NULL, ?, ?, ?, ?)"

annotations = [
	(1, 'chris', 0, 'cant be true'),
	(1, 'admin', 1, 'obviously true'),
	(2, 'chris', 1, 'might be true'),
	(3, 'chris', 0, 'definitely not true'),
	(5, 'user1', 1, 'i dunno')
]
cursor.executemany(insert_query, annotations)

print("Message: data.db was created. WARNING: If existing, duplicate values were inserted.")

connection.commit()
connection.close()
