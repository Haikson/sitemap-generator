import logging
import sqlite3


class SQLiteTodo(object):
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.__init_tables()

    def __init_tables(self):
        cursor = self.connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS todo_queue;")
        cursor.execute("""
            CREATE TABLE todo_queue (
                url text(1000) primary key
            );
        """)
        self.connection.commit()
        cursor.close()

    def add(self, url):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""insert into todo_queue values (?);""", (url,))
        except Exception as e:
            logging.info(e)
        finally:
            self.connection.commit()
            cursor.close()

    def remove(self, url):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""delete from todo_queue where url = ?;""", (url,))
        except Exception as e:
            logging.info(e)
        finally:
            self.connection.commit()
            cursor.close()

    def __contains__(self, item):
        cursor = self.connection.cursor()
        result = False
        try:
            cursor.execute("""select 1 from todo_queue where url = ?""", (item, ))
            row = cursor.fetchone()
            if len(row):
                result = True
        except Exception as e:
            logging.info(e)
        finally:
            cursor.close()
        return result

    def __iter__(self):
        cursor = self.connection.cursor()
        result = []
        try:
            cursor.execute("""select url from todo_queue""")
            rows = cursor.fetchall()
            result = [row[0] for row in rows]
        except Exception as e:
            logging.info(e)
        finally:
            cursor.close()
        return iter(result)

    def __next__(self):
        for url in self:
            yield url

    def __len__(self):
        cursor = self.connection.cursor()
        result = []
        try:
            cursor.execute("""select count(*) as cnt from todo_queue""")
            row = cursor.fetchone()
            result = row[0]
        except Exception as e:
            logging.info(e)
        finally:
            cursor.close()
        return result