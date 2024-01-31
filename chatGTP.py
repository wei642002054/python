import pymysql,os,time
from langchain import hub
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader, EverNoteLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
import numpy as np
from openai import OpenAI
from qdrant_client.models import PointStruct
from sshtunnel import SSHTunnelForwarder
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
class chatOpenAi():
    def __init__(self):
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["OPENAI_API_KEY"] = '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'
        self.qdrant_client = QdrantClient(host='60.205.180.69', port=6333)
        self.collection_name = 'my_collection'
        #链接数据库
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
    def close(self):
        self.cursor.close()  # 关闭查询
        self.db.close()
        self.server.close()  # 关闭服务
    def dbconnct(self):
        sql = "SELECT id,articleText FROM bloggerData_copy1"
        self.cursor.execute(sql)
        info = self.cursor.fetchall()
        self.close()
        # print(info[1][1])
        return info
    def searchDataBase(self,id):
        sql = 'select articleText from bloggerData_copy1 where id = {}'.format(id)
        self.cursor.execute(sql)
        info = self.cursor.fetchall()
        self.close()
        if info:
            return info[0][0]
        return None

    def truncate_text_tokens(self,text, encoding_name='cl100k_base', max_tokens=8191):
        import tiktoken
        encoding = tiktoken.get_encoding(encoding_name)
        return encoding.encode(text)[:max_tokens]
    def to_embeddings(self,items):
        client = OpenAI()
        sentence_embeddings = client.embeddings.create(
            model="text-embedding-ada-002",
            input=self.truncate_text_tokens(items)  #切割  最大显示8191
        )
        # print(sentence_embeddings.data[0].embedding)
        return sentence_embeddings.data[0].embedding

    def insertVector(self):
        self.qdrant_client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )
        points = [
                PointStruct(
                    # id=idx,
                    id = int(vector[0]),
                    # vector=vector.tolist(),
                    vector=self.to_embeddings(vector[1]),
                    # payload={"color": "red","text": vector[1]}
                )
                for idx, vector in enumerate(self.dbconnct())
            ]
        operation_info  = self.qdrant_client.upsert(  # insert
            collection_name=self.collection_name,
            wait=True,
            points=points
        )
        print(operation_info)
    def searchVector(self,issue):
        start = time.time()
        sentence_embeddings = self.to_embeddings(issue)
        search_result = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=np.array(sentence_embeddings),
                limit=1,
                # search_params={"exact": False, "hnsw_ef": 128}
            )
        first = time.time()
        print(first-start)
        for i in search_result:
            # print(i.payload['text'])
            articleText = self.searchDataBase(i.id) #查询数据库  源数据
            with open('Result.txt', 'w', encoding='utf-8') as file:
                file.write(str(articleText))
            raw_documents = TextLoader('Result.txt',encoding='utf-8').load()
            # print(raw_documents)
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            documents = text_splitter.split_documents(raw_documents)
            db = Chroma.from_documents(documents, OpenAIEmbeddings())
            retriever = db.as_retriever()
            prompt = hub.pull("rlm/rag-prompt")
            #llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0)  # "gpt-3.5-turbo"
            llm = ChatOpenAI(model_name="gpt-3.5-turbo-1106", temperature=0)  # "gpt-3.5-turbo"
            def format_docs(docs):
                print([doc.page_content for doc in docs])
                return "\n\n".join(doc.page_content for doc in docs)
            two = time.time()
            print(two-first)
            rag_chain = (
                    {"context": retriever | format_docs, "question": RunnablePassthrough()}
                    | prompt
                    | llm
                    | StrOutputParser()
            )
            reply = rag_chain.invoke(issue)
            print(reply)
        end = time.time()
        print(end-two)
        print('Total time: ' + str(end-start))
if __name__ == '__main__':
    issue = "创业时，什么时候该坚持，什么时候该转向"
    GTP = chatOpenAi()
    # GTP.insertVector()  #插入数据
    GTP.searchVector(issue)  #查询数据并回答
    
