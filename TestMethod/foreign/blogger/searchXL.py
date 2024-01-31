from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from openai import OpenAI
import random,time,os,pymysql
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sshtunnel import SSHTunnelForwarder
class chatInsert():
    def __init__(self):
        os.environ["http_proxy"] = "127.0.0.1:7890"
        os.environ["https_proxy"] = "127.0.0.1:7890"
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["OPENAI_API_KEY"] = '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'
        self.qdrant_client = QdrantClient(host='60.205.180.69', port=6333)
        self.collection_name = 'my_test'
        self.filePath = 'E:\PythonFile\Pycode10'
        # 链接数据库
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
        self.db = pymysql.connect(**mysql_config)
        self.cursor = self.db.cursor()
    def truncate_text_tokens(self, text, encoding_name='cl100k_base', max_tokens=8191):
        import tiktoken
        encoding = tiktoken.get_encoding(encoding_name)
        return encoding.encode(text)[:max_tokens]
    def close(self):
        self.cursor.close()  # 关闭查询
        self.db.close()
        self.server.close()  # 关闭服务
    def to_embeddings(self, items):
        client = OpenAI()
        sentence_embeddings = client.embeddings.create(
            model="text-embedding-ada-002",
            input=self.truncate_text_tokens(items)  # 切割  最大显示8191
            # input = items
        )
        # print(sentence_embeddings.data[0].embedding)
        return sentence_embeddings.data[0].embedding

    def cutting(self, content):  # 1000字符
        with open('Result.txt', 'w', encoding='utf-8') as file:
            file.write(str(content))
        raw_documents = TextLoader(self.filePath + '\\' + 'Result.txt', encoding='utf-8').load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        documents = text_splitter.split_documents(raw_documents)
        print(documents)
        return documents
    def dbconnct(self):
        sql = "SELECT id,articleText,title FROM bloggerData_copy1"
        self.cursor.execute(sql)
        info = self.cursor.fetchall()
        self.close()
        # print(info[1][1])
        return info

    def generate_unique_id(self):
        timestamp = int(time.time() * 1000)
        rand_num = random.randint(0, 1000)
        unique_id = '{}{}'.format(timestamp, rand_num)
        return unique_id
    def insertVector(self):
        self.qdrant_client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )
        points = [
            PointStruct(
                # id=idx,
                id=int(self.generate_unique_id()),
                # vector=vector.tolist(),
                vector=self.to_embeddings(content.page_content), #content.page_content|vector[1]
                payload={'DBID': vector[0], "title": vector[2], "text": content.page_content}
            )
            for idx, vector in enumerate(self.dbconnct())
            for content in self.cutting(vector[1])

        ]
        operation_info = self.qdrant_client.upsert(  # insert
            collection_name=self.collection_name,
            wait=True,
            points=points
        )
        print(operation_info)
if __name__ == '__main__':
    chatGPT = chatInsert()
    chatGPT.insertVector()