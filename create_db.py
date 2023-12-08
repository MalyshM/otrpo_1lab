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
    num_of_rounds INT,
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


def db_creation_and_fill_for_9_lab():
    conn = psycopg2.connect(dbname="otrpo_proj", user="postgres", password="admin",
                            host="db")
    cursor = conn.cursor()
    conn.autocommit = True
    sql1 = '''
    -- Create 10 users
INSERT INTO users (username, password, email, date_of_add)
VALUES
  ('user1', '$2b$12$bwkZF8CCgVnBLkbcOhFKe.4RShtX3VU7rUW83NOrxtF9MUb.iyIQC', 'user1@example.com', NOW()),
  ('user2', '$2b$12$bwkZF8CCgVnBLkbcOhFKe.4RShtX3VU7rUW83NOrxtF9MUb.iyIQC', 'user2@example.com', NOW()),
  ('user3', '$2b$12$bwkZF8CCgVnBLkbcOhFKe.4RShtX3VU7rUW83NOrxtF9MUb.iyIQC', 'user3@example.com', NOW()),
  ('user4', '$2b$12$bwkZF8CCgVnBLkbcOhFKe.4RShtX3VU7rUW83NOrxtF9MUb.iyIQC', 'user4@example.com', NOW()),
  ('user5', '$2b$12$bwkZF8CCgVnBLkbcOhFKe.4RShtX3VU7rUW83NOrxtF9MUb.iyIQC', 'user5@example.com', NOW()),
  ('user6', '$2b$12$bwkZF8CCgVnBLkbcOhFKe.4RShtX3VU7rUW83NOrxtF9MUb.iyIQC', 'user6@example.com', NOW()),
  ('user7', '$2b$12$bwkZF8CCgVnBLkbcOhFKe.4RShtX3VU7rUW83NOrxtF9MUb.iyIQC', 'user7@example.com', NOW()),
  ('user8', '$2b$12$bwkZF8CCgVnBLkbcOhFKe.4RShtX3VU7rUW83NOrxtF9MUb.iyIQC', 'user8@example.com', NOW()),
  ('user9', '$2b$12$bwkZF8CCgVnBLkbcOhFKe.4RShtX3VU7rUW83NOrxtF9MUb.iyIQC', 'user9@example.com', NOW()),
  ('user10', '$2b$12$bwkZF8CCgVnBLkbcOhFKe.4RShtX3VU7rUW83NOrxtF9MUb.iyIQC', 'user10@example.com', NOW());

-- Define the start and end dates of the 1-month range
DO $$
DECLARE
  StartDate DATE := CURRENT_DATE - INTERVAL '1 month';
  EndDate DATE := CURRENT_DATE;
  UserPokemons VARCHAR[] := ARRAY['first pokemon', 'second pokemon', 'third pokemon'];
  Winners VARCHAR[] := ARRAY['User', 'Computer'];
BEGIN
  -- Create 1000 Pokémon battles with random dates within the range
  FOR i IN 1..1000 LOOP
    DECLARE
      numOfRounds INT := ROUND(RANDOM() * 5) + 1;
      randomDays INT := ROUND(RANDOM() * (EndDate - StartDate));
      randomDate DATE := StartDate + randomDays;
      userPokemonIndex INT := FLOOR(RANDOM() * 3) + 1;
      computerPokemonIndex INT := FLOOR(RANDOM() * 3) + 1;
      winnerIndex INT := FLOOR(RANDOM() * 2) + 1;
    BEGIN
      INSERT INTO pokemon_battle (data, user_pokemon, computer_pokemon, winner, date_of_round, num_of_rounds, user_id)
      VALUES
        ('Battle Data', UserPokemons[userPokemonIndex], UserPokemons[computerPokemonIndex], Winners[winnerIndex], randomDate, numOfRounds, FLOOR(RANDOM() * 10) + 1);
    END;
  END LOOP;
END $$;
        '''
    cursor.execute(sql1)
    conn.commit()
    print("Database filled for 9 lab successfully........")

    # Closing the connection

    cursor.close()
    conn.close()


db_create()
db_creation_and_fill_for_9_lab()
