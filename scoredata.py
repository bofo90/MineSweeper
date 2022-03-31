
from configparser import ConfigParser
from numpy import insert
import psycopg2
from psycopg2 import Error

class Scores_Admin():

    def __init__(self):
        __info = self.__load_connection_info('db.ini')
        database_exist = self.create_db(__info)

        self.connection = psycopg2.connect(**__info)
        self.cursor = self.connection.cursor()

        if  not database_exist:
            self.create_tables()

        self.user_id = 0

    def __load_connection_info(self, ini_filename):
        parser = ConfigParser()
        parser.read(ini_filename)
        # Create a dictionary of the variables stored under the "postgresql" section of the .ini
        conn_info = {param[0]: param[1] for param in parser.items("postgresql")}
        return conn_info


    def create_db(self, conn_info):
        # Connect just to PostgreSQL with the user loaded from the .ini file
        psql_connection_string = f"user={conn_info['user']} password={conn_info['password']}"
        conn = psycopg2.connect(psql_connection_string)
        cur = conn.cursor()

        # "CREATE DATABASE" requires automatic commits
        conn.autocommit = True

        sql_query = f"SELECT datname FROM pg_catalog.pg_database WHERE datname = '{conn_info['database']}'"
        cur.execute(sql_query)
        exists = cur.fetchone()
        if exists == None:
            existance = False
            try:
                cur.execute(f"CREATE DATABASE {conn_info['database']}")
            except Exception as e:
                print('Error witht the database creation...')
            finally:
                conn.autocommit = False
        else:
            existance = True
        cur.close()
        conn.close()

        return existance

    def execute_query(self, sql_q, conn, cur):
        try:
            # Execute the table creation query
            cur.execute(sql_q)
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
            print(f"Query: {cur.query}")
            conn.rollback()
            cur.close()
        else:
            # To take effect, changes need be committed to the database
            conn.commit()

    def create_tables(self):
        table_users = """
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(200) UNIQUE NOT NULL,
                bot BOOL NOT NULL DEFAULT FALSE
            )
            """
        self.execute_query(table_users, self.connection, self.cursor)

        table_games =  """
            CREATE TABLE games (
                id SERIAL PRIMARY KEY,
                x_size INT NOT NULL,
                y_size INT NOT NULL,
                mines INT NOT NULL,
                id_user SERIAL REFERENCES users(id),
                time FLOAT NOT NULL,
                finished BOOL NOT NULL,
                cells_dest INT NOT NULL
            )
            """
        self.execute_query(table_games, self.connection, self.cursor)

    def close_connection(self):
        self.connection.close()
        self.cursor.close()

    def check_username(self, name):
        try:
            self.cursor.execute("SELECT * FROM users WHERE name = %(name)s", 
               {"name": name})
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
            print(f"Query: {self.cursor.query}")
        
        exist = self.cursor.fetchone()
        if exist != None:
            self.user_id = exist[0]
    
    def add_user(self, name, bot=False):
        insert_query = """ INSERT INTO users (name, bot) VALUES (%s, %s)"""
        values = (name, bot)
        self.cursor.execute(insert_query, values)
        self.connection.commit()
        self.check_username(name)

    def save_game(self, x, y, mines, time, win, score):
        insert_query = """ 
                INSERT INTO 
                games (x_size, y_size, mines, id_user, time, finished, cells_dest) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
        values = (x, y, mines, self.user_id, time, win, score)
        self.cursor.execute(insert_query, values)
        self.connection.commit()

    def get_user_best_games(self, x, y, mines):
        query = """
            SELECT u.name, g.cells_dest, g.time
            FROM games g
            JOIN users u
            ON u.id = g.id_user
            WHERE id_user = %s AND x_size = %s AND y_size = %s AND mines = %s 
            ORDER BY cells_dest DESC, time 
            LIMIT 5
            """
        values = (self.user_id, x, y, mines)
        self.cursor.execute(query, values)
        list_games = self.cursor.fetchall()
        return list_games
    
    def get_all_best_games(self, x, y, mines):
        query = """
            SELECT u.name, g.cells_dest, g.time
            FROM games g
            JOIN users u
            ON u.id = g.id_user
            WHERE x_size = %s AND y_size = %s AND mines = %s AND bot = %s
            ORDER BY cells_dest DESC, time
            LIMIT 5
            """
        values = (x, y, mines, False)
        self.cursor.execute(query, values)
        list_games = self.cursor.fetchall()
        return list_games