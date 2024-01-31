import csv,time
import pymysql
# 连接到 MySQL 数据库
from pymysql.converters import escape_string
from sshtunnel import SSHTunnelForwarder
class ReadMySql:
    def __init__(self):
        self.server = SSHTunnelForwarder(
            ssh_address_or_host=('aliyun-bj1.tongyuan.ai', 22),
            ssh_username='root',
            ssh_password='3HpvNIfT8WNZnAc4',
            remote_bind_address=('127.0.0.1', 3307)
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
    def readCsv(self,filePath,dataBash):
        # 读取 CSV 文件并将数据插入到数据库表中
        filename = filePath   # 替换为你的 CSV 文件路径
        table_name = dataBash  # 替换为你的目标数据库表名
        with open(filename, 'r',encoding='utf-8',errors='ignore') as file:
            csv_data = csv.reader(file)
            headers = next(csv_data)  # 获取 CSV 文件的列头
            # 构建 SQL 插入语句
            insert_query = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({', '.join(['%s']*len(headers))})"
            # print(insert_query)
            # time.sleep(3)
            # 逐行插入数据
            num = 0
            for row in csv_data:
                num+=1
                # if num < 4600:
                #     continue
                # print(row)
                row[10] = escape_string(str(row[10]))
                row[31] = escape_string(str(row[31]))
                try:
                    self.cursor.execute(insert_query, row)
                    print(f'正在插入{num}条')
                except:
                    print('错误跳过')
        # 提交更改并关闭数据库连接
        self.db.commit()
        print('已提交')
        self.cursor.close()
        self.db.close()
if __name__ == '__main__':
    filePath = r'E:\readFilePath\ElonMuskTwitter.csv'
    dbBash = 'ElonMuskTwitter'
    ReadMySql().readCsv(filePath,dbBash)