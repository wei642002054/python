import time
import pymysql  # 35服务  美国
import psycopg2
from sshtunnel import SSHTunnelForwarder
from multiprocessing.pool import ThreadPool
from multiprocessing.dummy import Pool
class AmericaInsertData(object):
    def __init__(self):
        self.mysql_config = {
            'user': 'root',
            'passwd': 'my-secret-pw',
            'host': '127.0.0.1',
            'port': 3306,
            'db': 'SpiderData',
        }
        # 连接数据库
        self.db = pymysql.connect(**self.mysql_config, connect_timeout=60)
        self.cursor = self.db.cursor()

    def close(self):
        self.cursor.close()  # 关闭查询
        self.db.close()
        # self.server.close()  # 关闭服务

    def replaceNone(self, d):  # 替换None空
        if isinstance(d, dict):
            for k in d:
                if d[k] is None:
                    d[k] = ''
                else:
                    AmericaInsertData().replaceNone(d[k])
        elif isinstance(d, list):
            for v in d:
                AmericaInsertData().replaceNone(v)

    def search_exists(self, databash, fieldName, uid):
        if self.db.open == False:
            self.db = pymysql.connect(**self.mysql_config, connect_timeout=60, autocommit=True, read_timeout=20)
            self.db.cursor()
        with self.db.cursor() as cursor:
            sql = f"SELECT * FROM {databash} where {fieldName} = '{uid}'"
            cursor.execute(sql)
            info = cursor.fetchall()
            if info != [] and info != ():
                self.cursor.close()
                self.db.close()
                return '已存在'
            self.cursor.close()
            self.db.close()
            return '未存在'

    def fetch_all(self, databash, data_dict, condition, uid):
        CREATETIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = f"SELECT * FROM {databash} where {condition} = '{uid}'"
        self.cursor.execute(sql)
        info = self.cursor.fetchall()
        if info != [] and info != ():
            print("已存在")
        else:
            data_dict['createTime'] = CREATETIME
            # InsertData().replaceNone(data_dict)
            zd = ",".join(data_dict.keys())  # Key 作为字段
            val = ",".join([f"'{x}'" for x in data_dict.values()])
            insert_sql = f"insert into {databash}({zd}) VALUES({val})"
            self.cursor.execute(insert_sql)
            self.db.commit()
            print('save to mysql successfully')
        self.cursor.close()
        self.db.close()

    def insertDirect(self, databash, data_dict):
        if self.db.open == False:
            self.db = pymysql.connect(**self.mysql_config, connect_timeout=60, autocommit=True, read_timeout=20)
            self.db.cursor()
        with self.db.cursor() as cursor:
            CREATETIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            data_dict['createTime'] = CREATETIME
            zd = ",".join(data_dict.keys())  # Key 作为字段
            val = ",".join([f"'{x}'" for x in data_dict.values()])
            insert_sql = f"insert into {databash}({zd}) VALUES({val})"
            cursor.execute(insert_sql)
            self.db.commit()
            print('save to mysql successfully')
            self.cursor.close()
            self.db.close()
            # self.close()

    def updata(self, databash, data_dict, condition, twitterId):
        data_dict['updateTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        key = data_dict.keys()  # Key 作为字段
        value = [f"'{x}'" for x in data_dict.values()]
        dataInfo = ",".join([i + '=' + str(v) for i, v in zip(key, value)])
        upsql = f"UPDATE {databash} SET {dataInfo} WHERE {condition} = {twitterId}"
        self.cursor.execute(upsql)
        self.db.commit()
        print('UPData to mysql successfully')
        self.cursor.close()
        self.db.close()
    def searchIP(self):
        if self.db.open == False:
            self.db = pymysql.connect(**self.mysql_config, connect_timeout=60, autocommit=True, read_timeout=20)
            self.db.cursor()
        with self.db.cursor() as cursor:
            sql = f"SELECT IpHost FROM roleIpPool"
            cursor.execute(sql)
            info = cursor.fetchall()
            IpAll = []
            for IP in info:
                IpAll.append(IP[0])
            self.cursor.close()
            self.db.close()
            return IpAll
    def deleteIp(self):
        if self.db.open == False:
            self.db = pymysql.connect(**self.mysql_config, connect_timeout=60, autocommit=True, read_timeout=20)
            self.db.cursor()
        with self.db.cursor() as cursor:
            try:
                query = f"SELECT * FROM roleIpPool ORDER BY id ASC LIMIT 30;"
                cursor.execute(query)
                result = cursor.fetchall()
                if len(result):
                    ids = [row[0] for row in result]
                    delete_query = f"DELETE FROM roleIpPool WHERE id IN ({','.join([str(id) for id in ids])});"
                    cursor.execute(delete_query)
                    self.db.commit()
                    print("成功删除了前30条数据。")
                else:
                    print("没有符合条件的数据需要删除。")
            except Exception as e:
                print('删除发生意外{}'.format(e))
            finally:
                self.cursor.close()
                self.db.close()

if __name__ == '__main__':
    print(AmericaInsertData().searchIP())