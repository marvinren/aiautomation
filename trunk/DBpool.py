# -*- coding: UTF-8 -*-
import logging

# import cx_Oracle
import MySQLdb
from DBUtils.PooledDB import PooledDB
import sys
from BasicFunction import *

reload(sys)
sys.setdefaultencoding('utf-8')


class DBSql(object):
    """
    数据库连接类
    """

    def __init__(self, conn_str, file_path=""):
        """
        初始化数据库，获取值
        :param connstr:数据库连接字串，"mysql=root#root#localhost#3306#taobaodb"
        :param filepath:文件路径，空为不执行
        """
        self.SQLS = {}
        # print conn_str
        self.dbtype = conn_str.split(":")[0]
        db_conn = conn_str.split(":")[1].split("/")
        self._connstr = {"user": db_conn[0], "password": db_conn[1], "host": db_conn[2], "port": db_conn[3],
                         "DB": db_conn[4], "charset": db_conn[5]}
        logging.info(self._connstr)
        self.dbpool = self._create_connection_pool()
        self.conn = self.dbpool.connection()
        # 游标不统一创建
        # self.cur = self.conn.cursor()
        if file_path != "":
            self._init_db_sql(file_path)

    def close(self):
        """
        关闭连接
        :return:
        """
        # self.cur.close()
        self.conn.close()

    def _init_db_sql(self, path):
        """
        获取数据库语句列表
        :param path:
        :return:
        """
        try:
            sql_file = open(path)
            for line in sql_file.readlines():
                _sqlInfo = line.split("==")
                self.SQLS[_sqlInfo[0]] = _sqlInfo[1][0:-1]
            print self.SQLS
        except Exception, e:
            print e
            print "open file error"

    def _create_connection_pool(self):
        """
        创建连接池
        :return:
        """
        if self.dbtype == 'oracle':
            # try:
            dsn = self._connstr["host"] + ":" + self._connstr["port"] + "/" + self._connstr["DB"]
            print dsn
            # pool = PooledDB(cx_Oracle, user=self._connstr["user"], password=self._connstr["password"], dsn=dsn,
            #                 threaded=True, mincached=CONFIG['mincached'], maxcached=CONFIG['maxcached'],
            #                 maxshared=CONFIG['maxshared'], maxconnections=CONFIG['poolsize'])
            # except Exception, e:
            #     raise Exception, 'conn targetdb datasource Excepts,%s!!!(%s).' % (self._connstr["host"], str(e))
            #     return None
        elif self.dbtype == 'mysql':
            try:
                pool = PooledDB(MySQLdb, user=self._connstr["user"], passwd=self._connstr["password"],
                                host=self._connstr["host"], port=int(self._connstr["port"]),
                                charset=self._connstr["charset"],
                                db=self._connstr["DB"], mincached=CONFIG['mincached'], maxcached=CONFIG['maxcached'],
                                maxshared=CONFIG['maxshared'], maxconnections=CONFIG['poolsize'])
                return pool
            except Exception, e:
                error = 'conn datasource Excepts,%s!!!(%s).' % (self._connstr["host"], str(e))
                logging.error(error)
                raise Exception(error)

    def update(self, sql):
        """
        数据库增删改
        :param sql: 数据库插入语句
        :return:
        """
        cur = None
        try:
            cur = self.conn.cursor()
            if type(sql) == list:
                for i in sql:
                    logging.info(i.decode('utf-8'))
                    cur.execute(i)
            elif type(sql) == str:
                logging.info(sql.decode('utf-8'))
                cur.execute(sql)
            elif type(sql) == unicode:
                logging.info(sql.decode('utf-8'))
                cur.execute(sql)
        except Exception, e:
            print e
            logging.error("execute:" + str(sql) + " ,ERROR")
        finally:
            self.conn.commit()
            if cur is not None:
                cur.close()

    def insert(self, sql):
        """
        数据库增
        :param sql: 数据库插入语句
        :return:
        """
        cur = self.conn.cursor()
        try:
            if type(sql) == list:
                for i in sql:
                    print '----start sql LIST-------'
                    print i
                    cur.execute(i)
                    print '----end sql LIST-------'
            elif type(sql) == str or type(sql) == unicode:
                print '----start sql STR-------'
                print sql
                cur.execute(sql)
                print '----end sql STR-------'
        except Exception, e:
            print e
            logging.error("execute:" + str(sql) + " ,ERROR")
        finally:
            cur.close()
            #   self.conn.commit()

    def commit(self):
        self.conn.commit()

    def get_sql_list(self, sql, num=0):
        """
        数据库查询,获取执行后结果
        :param num: 返回查询的数量
        :param sql: 数据库插入语句
        :return:二维元组
        """
        cur = self.conn.cursor()
        try:
            logging.info(sql.decode('utf-8'))
            cur.execute(sql)
            if num == 0:
                _result = cur.fetchall()
            else:
                _result = cur.fetchmany(num)
        except Exception, e:
            print e
            logging.debug("execute:" + sql + "   ,ERROR")
            _result = False
        finally:
            # self.conn.commit()
            cur.close()
            return _result

    def check_count(self, sql, count=1):
        """
        对比数据库中的条数是否与预期值相同
        :param sql: 数据库语句
        :param count:预期值
        :return:True，值相同，False，值不同
        """
        cur = self.conn.cursor()
        flag = True
        try:
            cur.execute(sql)
            num = cur.fetchone()[0]
            if num != count:
                flag = False
        except Exception, e:
            print e
            logging.debug("execute:" + sql + "   ,ERROR")
            flag = False
        finally:
            logging.debug('query count:' + str(num))
            cur.close()
            return flag

    def sql_from_file(self, name, *param):
        """
        根据文件中的标签拼接sql语句并执行
        :param name:标签
        :param param:对应与sql语句中的？
        :return:
        """
        cur = self.conn.cursor()
        if name in self.SQLS.keys():
            _sql = self.SQLS[name]
        else:
            return False
        sqls = _sql.split('?')
        sql_real = sqls[0]
        for i in range(1, len(sqls)):
            sql_real = sql_real + param[i - 1] + sqls[i]
        logging.debug(sql_real)
        try:
            cur.execute(sql_real)
        except Exception, e:
            print e
            logging.debug("execute:" + sql_real + "   ,ERROR")
            return False
        self.conn.commit()
        _result = cur.fetchall()
        cur.close()
        return _result

    def get_sql_first(self, sql):
        """
        获取select语句的第一个值
        :param sql:数据库语句
        :return:string/int
        """
        getinfo = self.get_sql_list(sql)
        # print getinfo
        logging.info('Result:' + str(getinfo))
        if not getinfo or len(getinfo) == 0:
            return ''
        else:
            try:
                return str(getinfo[0][0])
            except UnicodeEncodeError:
                return getinfo[0][0]
