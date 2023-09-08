from misc.singelton import SingletonMeta
from psycopg2 import connect
from ldubgdbot.bot.utils.env import Env


class Database(metaclass=SingletonMeta):

    def __init__(self):
        self.dbconn = connect(database=Env.database,
                              user=Env.username,
                              password=Env.password,
                              host=Env.host,
                              port='5432')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dbconn.close()

    def get_cursor(self):
        return self.dbconn.cursor()

    def get_connection(self):
        return self.dbconn
