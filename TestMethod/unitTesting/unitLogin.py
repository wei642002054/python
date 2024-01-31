from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,urllib3,requests,json,random,os
from selenium.webdriver.common.by import By
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
class loginRegistration:
    def __init__(self):
        self.proxy = {
            "https": "127.0.0.1:7890",
            "http": "127.0.0.1:7890"
        }
        self.ImgPath = r'E:\Img\rolePlayerNetImg'
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
    def generate_chinese_text(self,length): #随机生成中文
        text = ''
        for _ in range(length):
            char = chr(random.randint(0x4e00, 0x9fff))
            text += char
        return text
    def randomImg(self):# 文件列表随机选择一张图片
        file_list = []
        for root, dirs, files in os.walk(self.ImgPath):
            for file in files:
                if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".gif"):
                    file_path = os.path.join(root, file)
                    file_list.append(file_path)
        if len(file_list) > 0:
            selected_image = random.choice(file_list)
            return selected_image
        else:
            return r'E:\Img\rpnationImg\113940117677.jpg'
    def login(self):
        try:
            chrome_option = webdriver.ChromeOptions()
            # 隐身模式（无痕模式）参数 --incognito   无界面 --headless
            chrome_option.add_argument('--incognito')
            #最大化窗口参数
            chrome_option.add_argument('--start-maximized')
            #使用代理IP
            # chrome_option.add_argument('--proxy-server=http://202.20.16.82:9527')
            #消除："自动化控制提示" 的参数
            chrome_option.add_experimental_option('useAutomationExtension', False)
            chrome_option.add_experimental_option("excludeSwitches", ['enable-automation'])
            driver = webdriver.Chrome(options=chrome_option)
            driver.get("https://dev-hk.logenic.ai/")
            # driver.get("https://dev-hk.logenic.ai/auth/login")
            login_button = driver.find_element(By.XPATH,'//button[contains(text(), "Login")]')
            login_button.click() #提交
            time.sleep(2)  # 等待页面加载
            ## username_input = driver.find_element_by_name("username")
            username_input = driver.find_element(By.NAME,"username")
            password_input = driver.find_element(By.NAME,"password")
            username_input.send_keys("weimou" + Keys.RETURN)
            password_input.send_keys("Wei@199667" + Keys.RETURN)
            submit_button = driver.find_element(By.XPATH,'//button[contains(text(), "Continue")]')
            submit_button.click()
            time.sleep(3)  # 等待登录结果显示
            # self.creatorPortal(driver)  #
            print(driver.get_cookies(),'成功',driver.get_log('browser'))
            # 关闭浏览器驱动
            driver.quit()
        except Exception as e:
            print('xxxxx',e)
            # self.send_slack_info(f'登录时报错：{e}')
    def creatorPortal(self,driver):
        print(driver)
        creator = driver.find_element(By.XPATH,'//button[contains(text(), "Creator Portal")]')
        creator.click()
        # url = 'https://dev-hk.logenic.ai/agent'
        # driver.get(url)
        print('xxxxxxxxxx')
        creator = driver.find_element(By.XPATH,'//button[contains(text(), "Create")]')
        creator.click()
        print(driver.k)
        time.sleep(5)
        AgentName = self.generate_chinese_text(8)   #生成随机8位文字
        print(AgentName)
        driver.find_element(By.ID,'name').send_keys(AgentName)


        time.sleep(5)
if __name__ == '__main__':
    king = loginRegistration()
    king.login()
    # king.randomImg()
