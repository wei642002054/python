import time
from multiprocessing.pool import ThreadPool
from multiprocessing.dummy import Pool
import pymysql   #100服务上
from sshtunnel import SSHTunnelForwarder
class AmericaInsertData(object):
    def __init__(self):
        self.server = SSHTunnelForwarder(
            ssh_address_or_host=('la-h100.logenic.ai', 22),
            ssh_username='spider',
            ssh_password='t0Kop2vnWvIWM0GY',
            remote_bind_address=('127.0.0.1', 3306),

        )
        # 启动隧道服务
        self.server.start()
        self.mysql_config = {
            'user': 'root',
            'passwd': 'R_r6cihkiPe=nFYf:eHp',
            'host': '127.0.0.1',
            'port': self.server.local_bind_port,
            'db': 'SpiderData',

        }
        # 连接数据库
        self.db = pymysql.connect(**self.mysql_config,connect_timeout=60,
        autocommit=True,
        read_timeout=20)
        self.cursor = self.db.cursor()
    def close(self):
        self.cursor.close()  # 关闭查询
        self.db.close()
        self.server.close()  # 关闭服务
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
    def search_exists(self,databash,fieldName,uid):
        if self.db.open:
            sql = f"SELECT * FROM {databash} where {fieldName} = '{uid}'"
            self.cursor.execute(sql)
            info = self.cursor.fetchall()
            if info != [] and info != ():
                return '已存在'
            return '未存在'
        dbBash =pymysql.connect(**self.mysql_config,connect_timeout=60,
        autocommit=True,
        read_timeout=20)
        sql = f"SELECT * FROM {databash} where {fieldName} = '{uid}'"
        dbBash.cursor().execute(sql)
        info = dbBash.cursor().fetchall()
        if info != [] and info != ():
            return '已存在'
        return '未存在'
    def fetch_all(self, databash,data_dict,condition,uid):
        CREATETIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = f"SELECT * FROM {databash} where {condition} = '{uid}'"
        self.cursor.execute(sql)
        info = self.cursor.fetchall()
        if info != [] and info !=():
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
    def insertDirect(self,databash,data_dict):
        try:
            CREATETIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            data_dict['createTime'] = CREATETIME
            zd = ",".join(data_dict.keys())  # Key 作为字段
            val = ",".join([f"'{x}'" for x in data_dict.values()])
            insert_sql = f"insert into {databash}({zd}) VALUES({val})"
            self.cursor.execute(insert_sql)
            self.db.commit()
            print('save to mysql successfully')
            self.cursor.close()
            # self.db.close()
        except:
            self.close()  #pass掉
            self.db = pymysql.connect(**self.mysql_config, connect_timeout=60)
            self.cursor = self.db.cursor()
            CREATETIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            data_dict['createTime'] = CREATETIME
            zd = ",".join(data_dict.keys())  # Key 作为字段
            val = ",".join([f"'{x}'" for x in data_dict.values()])
            insert_sql = f"insert into {databash}({zd}) VALUES({val})"
            self.cursor.execute(insert_sql)
            self.db.commit()
            print('save to mysql successfully')
            self.cursor.close()
            self.db.close()
    def updata(self,databash,data_dict,condition,twitterId):
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
    def testInsert(self,data):
        while True:  # it works until the data was not saved
            try:
                db = self.db
                if db.open:
                    with db.cursor() as cursor:
                        print('xxxxxxxxxxxxxxxxxxxxxxxxx',data)
                        insert_sql = f"insert into rolePlayImage (post_id) VALUES({data})"
                        cursor.execute(insert_sql)
                        db.commit()
                        print('save to mysql successfully')
                        # self.cursor.close()
                    break
            except:
                print('断开重试',self.db.open)
                dbBash =pymysql.connect(**self.mysql_config,connect_timeout=60,
        autocommit=True,
        read_timeout=20)
                with dbBash.cursor() as cursor:
                    print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxzzzzz',data)
                    insert_sql = f"insert into rolePlayImage (post_id) VALUES({data})"
                    cursor.execute(insert_sql)
                    dbBash.commit()
                    print('save to mysql successfully')
                    cursor.close()
                    dbBash.close()
                break
if __name__ == '__main__':

    dbbash = 'rolePlayImage'
    pool = ThreadPool(8) # 线程
    # pool = Pool(processes=4)  #进程
    for i in range(0,3000):
        # AmericaInsertData().testInsert(str(i))
        pool.map(AmericaInsertData().testInsert, str(i))
    pool.close()
    pool.join()