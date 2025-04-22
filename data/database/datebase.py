# Database setup function
import sqlite3


def create_sample_database(database_name):
    """创建一个新的数据库来暂存一些内容"""
    def create_sqlite_database(filename):
        conn = None
        try:
            conn = sqlite3.connect(filename)
            print('数据库新建成功')
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
