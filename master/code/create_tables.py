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

print(users)

create_table = "CREATE TABLE IF NOT EXISTS edges (ref INTEGER PRIMARY KEY, exposure int, exp_name text, outcome int, out_name text, MRestimate real)"
cursor.execute(create_table)

insert_query = "INSERT INTO edges VALUES (NULL, ?, ?, ?, ?, ?)"

edges = [
	(1, 'Adiponectin', 10, 'Crohns_disease', 0.001),
	(1, 'Adiponectin', 100, 'Hip_circumfrance', 0.002),
	(1, 'Adiponectin', 1000, 'Depressive_symptoms', 0.003),
	(10, 'Crohns_disease', 100, 'Hip_circumfrance', 0.004),
	(10, 'Crohns_disease', 1000, 'Depressive_symptoms', 0.005),
	(100, 'Hip_circumfrance', 1000, 'Depressive_symptoms', 0.006)	
]
cursor.executemany(insert_query, edges)

print(edges)

create_table = "CREATE TABLE IF NOT EXISTS annotations (annotID INTEGER PRIMARY KEY, ref int, username text, judgement int, comment text)"
cursor.execute(create_table)

insert_query = "INSERT INTO annotations VALUES (NULL, ?, ?, ?, ?)"

annotations = [
	(1, 'chris', 0, 'cant be true'),
	(1, 'chris', 1, 'actually it could be'),
	(2, 'chris', 0, 'definitely not true')
]
cursor.executemany(insert_query, annotations)

print(annotations)

connection.commit()
connection.close()
