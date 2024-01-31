from sshtunnel import SSHTunnelForwarder
import os, pymysql,time
class onLineMySqlSSH:  # 001 服务上
    def __init__(self):
        self.server = SSHTunnelForwarder(
            ssh_address_or_host=('dev-hk.logenic.ai', 22),
            ssh_username='wjf',
            ssh_password='wjf',
            remote_bind_address=('127.0.0.1', 3306)
        )

        # 启动隧道服务
        self.server.start()

        mysql_config = {
            'user': 'root',
            'passwd': 'R_r6cihkiPe=nFYf:eH',
            'host': '127.0.0.1',
            'port': self.server.local_bind_port,
            'db': 'agent_platform_web',
        }
        # 连接数据库
        self.db = pymysql.connect(**mysql_config)
        self.cursor = self.db.cursor()
    def fetch_one(self,databash,fieldName,uid):
        sql = f"SELECT * FROM {databash} where {fieldName} = '{uid}'"
        self.cursor.execute(sql)
        info = self.cursor.fetchall()
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
    def searchTwitter(self,databash):
        #SELECT * from twitterPosts GROUP BY twitterName
        sql = f"SELECT * FROM {databash}"
        self.cursor.execute(sql)
        info = self.cursor.fetchall()
        print('info',info)
        # num = 0
        # Url_dict = []
        # for row in info:
if __name__ == '__main__':
    twitterData = onLineMySqlSSH()
    databash = 'agents'#
    twitterData.searchTwitter(databash,)