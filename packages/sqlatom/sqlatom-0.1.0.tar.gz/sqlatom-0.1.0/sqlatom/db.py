# coding=utf8
from collections import namedtuple
from sqlatom import DBEngine
from MySQLdb import string_literal
from datetime import datetime

OrderByCriteria = namedtuple('OrderByCriteria', ['column', 'order'])
WhereCriteria = namedtuple('WhereCriteria', ['column', 'op', 'value'])


def chainmap(*m):
    d = {}
    for mm in m:
        d.update(mm)
    return d


def literal(v):
    """
    :param v: variable for literal
    :return: str, literal expression
    """
    if v is None:
        return 'null'
    elif isinstance(v, unicode):
        return string_literal(v.encode('utf8')).decode('utf8')
    elif isinstance(v, (str, bytes)):
        return string_literal(v).decode('utf8')
    elif isinstance(v, long):
        return str(v)
    elif isinstance(v, datetime):
        return repr(v.strftime('%Y-%m-%d %H:%M:%S'))
    else:
        return repr(v)


class QueryBuilder:
    """Query Builder
    """

    def __init__(self, engine, table):
        self._engine = engine
        self._table = table
        self._reset()

    def _reset(self):
        self._select_columns = None
        self._offset = None
        self._limit = None
        self._orderby_criterion = []
        self._where_criterion = []

    def name(self):
        return self._table

    def select(self, *columns):
        """
        :param columns: ...str, column names
        :return:
        """
        self._select_columns = columns
        return self

    def insert(self, kvs):
        """
        :param kvs: dict, kv of column to value
        :return: int, row id which has been inserted
        """
        if self._where_criterion:
            raise Exception('SQLBuilder.insert cannot has where criterion')

        buff = self._insert_kvs_sql_buffer(kvs)
        sql = ' '.join(buff)
        self.on_execute(sql)
        return self._engine.insert(sql)

    def insertOrIgnore(self, kvs):
        """
        :param kvs: dict, kv of column to value
        :return: int, row id which has been inserted
        """
        if self._where_criterion:
            raise Exception('SQLBuilder.insert cannot has where criterion')

        buff = self._insert_kvs_sql_buffer(kvs)
        buff = buff[:1] + ['IGNORE'] + buff[1:]
        sql = ' '.join(buff)
        self.on_execute(sql)
        return self._engine.insert(sql)

    def getOrCreate(self, insert_kvs={}):
        """
        1. select by where criterion if exists, otherwise...
        2. insert value (`insert_kvs`, inner where criterion)

        :param insert_kvs: dict, kv of column to value
        :return: dict, row data as dict
        """
        for c in self._where_criterion:
            if c.op != '=':
                raise Exception('SQLBuilder.getOrCreate only compatible with "=" where criteria')

        rv = self.first()
        if rv is not None:
            return rv

        m = chainmap(insert_kvs, {c.column: c.value for c in self._where_criterion})
        m['id'] = self.insert(m)
        return m

    def insertOrUpdate(self, insert_kvs, update_cols=None, update_kvs={}):
        """
        :param insert_kvs: dict, insert kv
        :param update_cols: List[str], constrain update column
        :param update_kvs: dict, higher priority then insert_kvs when do update
        :return: dict, row data as dict

        1. insert all `insert_kvs`, otherwise...
        2. use `update_cols` or all keys in `insert_keys` as update_column
        3. get all value from (`update_kvs`, 'insert_kvs') by update_column
        4. do update

        for example: table has three column: title, slug(unique), body

        a. insert (title, slug, body) or update (title, slug, body)
        insertOrUpdate({title: 'hello', slug: 'hello', body: 'hello world'})
        is brief with
        insertOrUpdate({title: 'hello', slug: 'hello', body: 'hello world'}, [title, slug, body])

        b. insert (title, slug, body) or update (body)
        insertOrUpdate({title: 'hello', slug: 'hello', body: 'hello world'}, [body])

        c. insert (title, slug, body) or update (body='different')
        insertOrUpdate({title: 'hello', slug: 'hello', body: 'hello world'}, [body], {body: 'different'})

        sql syntax:
        insert into table(col, col) values (val, val) on duplicate key update col=val, col=val;
        """
        if self._where_criterion:
            raise Exception('SQLBuilder.insert cannot has where criterion')

        buff = self._insert_kvs_sql_buffer(insert_kvs)
        buff.append('ON DUPLICATE KEY UPDATE')

        m = chainmap(update_kvs, insert_kvs)
        kvs = {k: m[k] for k in (update_cols or insert_kvs.keys())}
        buff.append(self._update_kvs_sql(kvs))
        sql = ' '.join(buff)
        self.on_execute(sql)
        return self._engine.execute(sql)

    def updateOrInsert(self, update_kvs, insert_kvs={}):
        """
        :param update_kvs: dict, update kv
        :param insert_kvs: dict, insert kv
        :return: dict, row data as dict

        1. update `update_kvs` by where criterion if exists, otherwise...
        2. insert all value (`insert_kvs`, `update_kvs`, inner where criterion)
        """
        for c in self._where_criterion:
            if c.op != '=':
                raise Exception('SQLBuilder.getOrCreate only compatible with "=" where criteria')

        n = self.update(update_kvs)
        if n > 0:
            return n

        m = chainmap(insert_kvs, update_kvs, {c.column: c.value for c in self._where_criterion})
        return self.insert(m)

    def _insert_kvs_sql_buffer(self, kvs):
        """
        :param kvs: dict, kv of column and value
        :return: List[str], buff for build sql statement
        """
        kv_list = list(kvs.items())
        key_list = [kv[0] for kv in kv_list]
        val_list = [literal(kv[1]) for kv in kv_list]

        return ['INSERT', 'INTO', self._table, '(' + ', '.join(key_list) + ')', 'VALUES',
                '(' + ','.join(val_list) + ')']

    def delete(self):
        """
        :return: int, effect row count
        """
        buff = ['DELETE FROM' + ' ' + self._table]
        where_sql = self._where_sql()
        if where_sql:
            buff.append('WHERE')
            buff.append(where_sql)

        sql = ' '.join(buff)
        self.on_execute(sql)
        self._engine.execute(sql)

    def update(self, kvs):
        """
        :param kvs: dict, key values for update
        :return: int, effect row count
        """
        buff = ['UPDATE', self._table, 'SET', self._update_kvs_sql(kvs)]
        where_sql = self._where_sql()
        if where_sql:
            buff.append('WHERE')
            buff.append(where_sql)

        sql = ' '.join(buff)
        self.on_execute(sql)
        return self._engine.execute(sql)

    def _update_kvs_sql(self, kvs):
        """
        :param kvs: kv of column and value
        :return: str, part of sql statement
        """
        buff = []
        for key, val in kvs.items():
            buff.append(key + ' = ' + literal(val))
        return ', '.join(buff)

    def first(self):
        """
        :return: first row data
        """
        buff = ['SELECT' + ' ' + self._select_column_sql()] + self._select_sql_buffer()
        sql = ' '.join(buff)
        self.on_execute(sql)
        return self._engine.select_one(sql)

    def all(self):
        """
        :return: Iterable, iterator of rows
        """
        buff = ['SELECT' + ' ' + self._select_column_sql()] + self._select_sql_buffer()
        sql = ' '.join(buff)
        self.on_execute(sql)
        return self._engine.select_all(sql)

    def count(self):
        """
        :return: int, row count
        """
        buff = ['SELECT COUNT(*)'] + self._select_sql_buffer()
        sql = ' '.join(buff)
        self.on_execute(sql)
        return self._engine.select_one(sql)

    def where(self, column, *args):
        """
        :param column: str, column name
        :param args: value or op-value
        :return: self

        where(id, '==', 10)
        where('id', 10)
        """
        if len(args) == 1:
            self._where_criterion.append(WhereCriteria(column=column, op='=', value=args[0]))
        elif len(args) == 2:
            self._where_criterion.append(WhereCriteria(column=column, op=args[0], value=args[1]))
        else:
            raise Exception('QueryBuilder.where must pass 2 or 3 parameter')
        return self

    def whereRaw(self, expr):
        """
        :param expr: str, part of sql where
        :return: self
        """
        self._where_criterion.append(WhereCriteria(column=None, op=None, value=expr))
        return self

    def _select_column_sql(self):
        """
        :return: str, column name part of select sql statement
        """
        if self._select_columns:
            return ', '.join(self._select_columns)
        return '*'

    def _where_sql(self):
        """
        :return: str, where part of sql statement
        """
        buff = []
        for c in self._where_criterion:
            if c.column is None:
                buff.append(c.value)
            else:
                buff.append(c.column + ' ' + c.op + ' ' + literal(c.value))
        return ' AND '.join(buff)

    def _order_sql(self):
        """
        :return: str, order part of sql statment
        """
        buff = []
        for c in self._orderby_criterion:
            buff.append(c.column + ' ' + c.order.upper())
        return ', '.join(buff)

    def _select_sql_buffer(self):
        buff = ['FROM', self._table]

        where_sql = self._where_sql()
        if where_sql:
            buff.append('WHERE')
            buff.append(where_sql)

        orderby_sql = self._order_sql()
        if orderby_sql:
            buff.append('ORDER BY')
            buff.append(orderby_sql)

        if self._limit:
            buff.append('LIMIT')
            buff.append(str(self._limit))

        if self._offset:
            buff.append('OFFSET')
            buff.append(str(self._offset))

        return buff

    def skip(self, n):
        """
        :param n: int,
        :return:
        """
        return self.offset(n)

    def offset(self, n):
        """
        :param n: int,
        :return:
        """
        self._offset = n
        return self

    def take(self, n):
        """
        :param n: int,
        :return:
        """
        return self.limit(n)

    def limit(self, n):
        """
        :param n: int,
        :return:
        """
        self._limit = n
        return self

    def orderBy(self, column, direction='ASC'):
        """
        :param column: str, column name
        :param direction: str, direction of order,
        :return:
        """
        self._orderby_criterion.append(OrderByCriteria(column, direction.upper()))
        return self

    def on_execute(self, sql):
        self._reset()


class DB:
    """
    DB.table('test').insert({'id': 123})
    DB.table('test').select('id').get();
    DB.table('test).where('abc').get();
    """

    engine = None

    def __init__(self, host='127.0.0.1', port=3306, user='root', passwd='', db=''):
        """
        :param host: str
        :param port: int
        :param user: str
        :param passwd: str
        :param db: str
        """
        self.engine = DBEngine(host=host, port=port, user=user, passwd=passwd, db=db)

    @classmethod
    def init(cls, host='127.0.0.1', port=3306, user='root', passwd='', db=''):
        """
        :param host: str
        :param port: int
        :param user: str
        :param passwd: str
        :param db: str
        """
        cls.engine = DBEngine(host=host, port=port, user=user, passwd=passwd, db=db)

    @classmethod
    def table(cls, name):
        return QueryBuilder(cls.engine, name)

    # def table(self, name):
    #    return QueryBuilder(self.engine, name)
