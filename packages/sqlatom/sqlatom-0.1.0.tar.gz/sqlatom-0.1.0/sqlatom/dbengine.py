# coding=utf8

import MySQLdb
from contextlib import closing
from typing import List, Any


class DBEngine:
    def __init__(self, host='127.0.0.1', port=3306, user='root', passwd='', db=''):
        """
        initialize database connection
        :param host: str
        :param port: int
        :param user: str
        :param passwd: str
        :param db: str
        """
        self.conn = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=db, autocommit=True,
                                    charset='utf8mb4')

    @property
    def dictCursor(self):
        return self.conn.cursor(MySQLdb.cursors.DictCursor)

    @property
    def cursor(self):
        return self.conn.cursor()

    def select_one(self, sql, args=None):
        """
        select only one row from db

        :param sql: sql statement with placeholder '%s'
        :param args: tuple or list
        :return: dict
        """
        with closing(self.dictCursor) as c:
            c.execute(sql, args=args)
            return c.fetchone()

    def select_all(self, sql, args=None):
        """
        select all row from db

        :param sql: sql statement with placeholder '%s'
        :param args: tuple or list
        :return: List[dict]
        """
        with closing(self.dictCursor) as c:
            c.execute(sql, args=args)
            return c.fetchall()

    def select_n(self, n, sql, args=None):
        """
        select limit n rows

        :param n: int
        :param sql: sql statement with placeholder '%s'
        :param args: tuple or list
        :return: List[dict]
        """
        with closing(self.dictCursor) as c:
            c.execute(sql, args=None)
            if n == -1:
                return c.fetchall()
            else:
                return c.fetchmany(n)

    def select(self, sql, args=None):
        """
        :param sql: sql statement with placeholder '%s'
        :param args: tuple or list
        :return: dict
        """
        return self.select_one(sql, args=args)

    def execute(self, sql, args=None):
        """
        :param sql: sql statement with placeholder '%s'
        :param args: tuple or list
        :return: int, effect row count
        """
        with closing(self.cursor) as c:
            c.execute(sql, args=args)
            return c.rowcount

    def insert(self, sql, args=None):
        """
        :param sql: sql statement with placeholder '%s'
        :param args: tuple or list
        :return: int, row id which has been inserted
        """
        with closing(self.cursor) as c:
            c.execute(sql, args=args)
            return c.lastrowid
