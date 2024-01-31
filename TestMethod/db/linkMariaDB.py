from sqlalchemy.testing.plugin.plugin_base import logging
from sshtunnel import SSHTunnelForwarder
import os, pymysql,time
# from TestMethod.public.initLog import init_log_config

class MySqlSSH:
    def __init__(self):
        self.server = SSHTunnelForwarder(
            ssh_address_or_host=('aliyun-bj1.tongyuan.ai', 22),
            ssh_username='root',
            ssh_password='3HpvNIfT8WNZnAc4',
            remote_bind_address=('127.0.0.1', 3307),
        )

        # 启动隧道服务
        self.server.start()

        mysql_config = {
            'user': 'root',
            'passwd': 'my-secret-pw',
            'host': '127.0.0.1',
            'port': self.server.local_bind_port,
            'db': 'SpiderData',

        }

        # 连接数据库
        self.db = pymysql.connect(**mysql_config)
        self.cursor = self.db.cursor()

    def fetch_one(self,databash,fieldName,uid):
         try:
            sql = f"SELECT * FROM {databash} where {fieldName} = '{uid}'"
            self.cursor.execute(sql)
            info = self.cursor.fetchall()
            if info != [] and info != ():
                return '已存在'
            return '未存在'
         except:
            print('查询出现问题')
            self.db.ping(True)
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
            self.db.close()
        except:
            print('插入出现问题')
            self.db.ping(True)
    def execute_sql(self,databash,data_dict,uid):
        CREATETIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = f"SELECT * FROM {databash} where url = '{uid}'"
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

    def close(self):
        self.cursor.close()  # 关闭查询
        self.db.close()
        self.server.close()  # 关闭服务
    def querySql(self,databash,uid):  #查询是否存在
        sql = f"SELECT * FROM {databash} where twitterId = '{uid}'"
        self.cursor.execute(sql)
        info = self.cursor.fetchall()
        if info != [] and info !=():
            return '已存在'
        return '未存在'
    def conn_mysql(self,databash,data_dict,uid):
        CREATETIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = f"SELECT * FROM {databash} where twitterId = '{uid}'"
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
    def getFinally(self,databash,columns):  #返回查询最后一个token
        # sql = 'SELECT * FROM twitterShare'
        sql = f"SELECT * FROM {databash} ORDER BY {columns} DESC LIMIT 1;"
        self.cursor.execute(sql)
        info = self.cursor.fetchall()
        # num = 0
        # Url_dict = []
        # for row in info:
        #     num +=1
        #     # print(num,row[7])
        #     Url_dict.append((row[1],row[7]))
        # return Url_dict
        return info[0][4]   #返回查询最后一个token
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