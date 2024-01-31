from multiprocessing.pool import ThreadPool,Pool
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,urllib3,requests,json,random,os
from selenium.webdriver.common.by import By
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
class socketError:
    def __init__(self):
        self.proxy = {
            "https": "127.0.0.1:7890",
            "http": "127.0.0.1:7890"
        }
        self.CREATETIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    def send_slack_info(self,message, channel='weberror'):
        webhook_url = 'https://hooks.slack.com/services/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'
        # 将您的消息封装成一个 JSON 格式的负载，同时指定频道
        payload = {
            'text': message,
            'channel': f'#{channel}'  # 请确保您的 Webhook 允许向该频道发送消息
        }
        requests.post(         # 发送 POST 请求
            webhook_url, proxies=self.proxy, data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
    def resultSpider(self,page=0):
        try:
            chrome_option = webdriver.ChromeOptions()
            # 隐身模式（无痕模式）参数 --incognito   无界面 --headless
            chrome_option.add_argument('--incognito')
            # 最大化窗口参数
            chrome_option.add_argument('--start-maximized')
            # 使用代理IP
            # chrome_option.add_argument('--proxy-server=http://202.20.16.82:9527')
            # 消除："自动化控制提示" 的参数
            chrome_option.add_experimental_option('useAutomationExtension', False)
            chrome_option.add_experimental_option("excludeSwitches", ['enable-automation'])
            driver = webdriver.Chrome(options=chrome_option)
            # url = 'http://192.168.0.112:3000/check?username=zhangyuge2022&password=Peikang2017.'
            url = "https://dev-hk.logenic.ai/check?username=zhangyuge2022&password=Peikang2017."
            driver.get(url)
            time.sleep(30)
            result = driver.find_elements(By.XPATH,'//*[@id="__next"]/div/div[2]/table/tbody/tr')
            error = []
            for i in result: #success
                if 'failed' in i.text or 'wait' in i.text: #failed
                    error.append(i.text.replace('\n',','))
                print(page,i.text)
            driver.quit()
            if error:
                self.send_slack_info(f'{self.CREATETIME}-->报错信息：{error}')
        except Exception as e:
            self.send_slack_info(f'{self.CREATETIME}-->报错信息(服务)：{e}')
if __name__ == '__main__':
    numPage = []
    for i in range(0,6):
        numPage.append(i)
    king = socketError()
    # king.resultSpider()
    pool = Pool(processes=6)
    pool.map(king.resultSpider, numPage)
    pool.close()
    pool.join()
