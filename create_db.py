import psycopg2


def db_create():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="admin", host="db")
    cursor = conn.cursor()

    conn.autocommit = True
    sql = '''DROP DATABASE IF EXISTS otrpo_proj;'''
    cursor.execute(sql)
    sql = '''CREATE DATABASE otrpo_proj
            WITH 
            OWNER = postgres
            ENCODING = 'UTF8'
            TABLESPACE = pg_default
            CONNECTION LIMIT = -1;'''
    try:
        cursor.execute(sql)
    except psycopg2.Error as e:
        print("Error creating database:", e)
    conn.commit()
    cursor.close()
    conn.close()
    conn = psycopg2.connect(dbname="otrpo_proj", user="postgres", password="admin",
                            host="db")
    cursor = conn.cursor()
    conn.autocommit = True
    sql1 = '''
DROP TABLE IF EXISTS pokemon_battle CASCADE;
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR,
    email VARCHAR(255),
    date_of_add TIMESTAMP
);
CREATE TABLE pokemon_battle (
    id SERIAL PRIMARY KEY,
    data VARCHAR(255),
    user_pokemon VARCHAR(255),
    computer_pokemon VARCHAR(255),
    winner VARCHAR(255),
    date_of_round TIMESTAMP,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
    '''
    cursor.execute(sql1)
    conn.commit()
    print("Database created successfully........")

    # Closing the connection

    cursor.close()
    conn.close()


db_create()
