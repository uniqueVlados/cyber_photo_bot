import sqlite3

conn = sqlite3.connect('users.db')

cursor = conn.cursor()


class Db:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS users (
        tg_id INTEGER,
        state TEXT);
        ''')

        self.conn.commit()

    def add_user(self, tg_id, state):
        insert_query = '''
            INSERT INTO users (tg_id, state)
            VALUES (?, ?);
        '''

        user_data = (tg_id, state)
        self.cursor.execute(insert_query, user_data)
        self.conn.commit()

    def set_state_user(self, tg_id, state):
        sql = '''UPDATE users SET state = ? WHERE tg_id = ?'''
        self.cursor.execute(sql, (state, tg_id))
        self.conn.commit()

    def get_state_user(self, tg_id):
        sql = f"SELECT state FROM users WHERE tg_id={tg_id}"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result[0]

    def check_user(self, tg_id):
        sql = f"SELECT state FROM users WHERE tg_id={tg_id}"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return False