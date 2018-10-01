import mysql.connector
from mysql.connector import errorcode
import db.database_config as db

DB_NAME = db.get_db_name()
TABLES = {}

TABLES['id_queue'] = (
    "CREATE TABLE `id_queue` ("
    "  `uid` int(11) NOT NULL AUTO_INCREMENT,"
    "  `id` varchar(128) NOT NULL,"
    "  `next_id` varchar(128) NOT NULL,"
    "  `count` int(11) NOT NULL DEFAULT 0,"
    "  `area` int(11) NOT NULL DEFAULT 0,"
    "  `next_area` int(11) NOT NULL DEFAULT 0,"
    "  PRIMARY KEY (`uid`)"
    ") ENGINE=InnoDB")

TABLES['detail'] = (
    "CREATE TABLE `detail` ("
    "  `uid` int(11) NOT NULL AUTO_INCREMENT,"
    "  `id` varchar(128) NOT NULL,"
    "  `detail` text(30000) NOT NULL,"
    "  PRIMARY KEY (`uid`)"
    ") ENGINE=InnoDB")


class Db:
    def __init__(self):
        '''
        初始化，连接并创建数据库、表
        '''
        self.cnx = mysql.connector.connect(user='root', host=db.get_host(), password=db.get_password())
        self.cursor = self.cnx.cursor()
        try:
            self.cnx.database = DB_NAME
        except Exception as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                try:
                    self.cursor.execute(
                        "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME)
                    )
                except mysql.connector.Error as err:
                    print('Fail to create database:'.format(DB_NAME))
                    exit(-1)
                self.cnx.database = DB_NAME
            else:
                print(err)
                exit(-1)
        # 数据表
        for name, ddl in TABLES.items():
            try:
                print("Creating table {}: ".format(name), end='')
                self.cursor.execute(ddl)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("table {} already exists.".format(name))
                else:
                    print(err.msg)
            else:
                print("all tables was be established")

    def insert_count(self, count):
        add_count = ("INSERT INTO id_queue"
                     "(count)"
                     "VALUES (%s)")
        self.cursor.execute(add_count, count)

    def insert_id(self, id, next_id, count, area, next_area):
        # sql语句
        add_id = ("INSERT INTO id_queue"
                  "(id, next_id, count, area, next_area)"
                  "VALUES (%s, %s, %s, %s, %s)")
        self.cursor.execute(add_id, id, next_id, count, area, next_area)

    def insert_detail(self, id, detail):
        add_detail = ("INSERT INTO detail"
                      "(id, detail)"
                      "VALUES (%s, %s)")
        self.cursor.execute(add_detail, id, detail)