import ddddocr
import execjs
import urllib3
import ssl,re
import random
import requests
from PIL import Image
from multiprocessing import Pool
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context
class sudokuVerify:
    def __init__(self):
        self.url = 'https://beijing.baixing.com/oz/s9verify_html'
        self.proxy = {
            "https": "127.0.0.1:7890",
            "http": "127.0.0.1:7890"
        }
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        self.node = execjs.get()
        self.file_js = 'E:\PythonFile\PyCode\TestMethod\ExJsFile\Sudoku.js'
        self.ImgFile = 'E:\PythonFile\PyCode\TestMethod\ExJsFile'
    def JsVerify(self):
        ctx = self.node.compile(open(self.file_js,encoding='utf-8').read())
        cookieData = ctx.eval('getFirstParams()')
        s = 'c0fc276cce08ba22dc='+cookieData['s']+';'
        f ='c1fc276cce08ba22dc='+cookieData['f']+';'
        bxf = 'bxf='+cookieData['f']
        trackCity = self.headers['Cookie']+';'
        self.headers['Cookie'] = trackCity+s+f+bxf
    def firstVerify(self):
        resp = requests.get(url=self.url,proxies=self.proxy,headers=self.headers,verify=False)
        set_cookie = resp.headers["Set-Cookie"]
        trackId = ''.join(re.findall('(__trackId.*?);',str(set_cookie),re.S)).strip()
        city = ''.join(re.findall('(__city.*?);',str(set_cookie),re.S)).strip()
        jsUlr = 'https://beijing.baixing.com/shield/bf.js'
        self.headers['Cookie']=trackId+';'+city
        requests.get(url=jsUlr,proxies=self.proxy,headers=self.headers,verify=False)
        print(self.headers['Cookie'])
        self.JsVerify() #Cookie验证
        print(self.headers['Cookie'])
        respon = requests.get(url=self.url,headers=self.headers,proxies=self.proxy,verify=False)
        jsSite = 'https:'+''.join(re.findall('</script><.*?src=\'(.*?).js\?mobi=n',respon.text,re.S)).strip()+'.js?mobi=n'
        jsResp = requests.get(url=jsSite,headers=self.headers,proxies=self.proxy,verify=False)
        jsResp.encoding=jsResp.apparent_encoding
        imgNumber = ''.join(re.findall('次点击.*?>(.*?)<',jsResp.text,re.S)).strip()
        backdrop = jsSite.replace('.js?','.jpg?') #需要点击的数字、
        validUrl = jsSite.replace('.js?','.valid?')
        Imgresp = requests.get(url=backdrop, headers=self.headers, proxies=self.proxy,verify=False, timeout=18)
        with open(self.ImgFile+'\loser.jpg',"wb") as f:  # 下载封面
            f.write(Imgresp.content)
        print(imgNumber)
        print(backdrop)
        return list(map(int,imgNumber.split('-'))),validUrl
    def imgsortSpider(self):
        captcha = Image.open(self.ImgFile+"/loser.jpg")
        # # 将图片等分成三份，每份长宽为 150px 和 50px
        part1 = captcha.crop((0, 0, 150, 50))
        part2 = captcha.crop((0, 50, 150, 100))
        part3 = captcha.crop((0, 100, 150, 150))
        part1.save("part1.jpg")
        part2.save("part2.jpg")
        part3.save("part3.jpg")
        # 创建新的图片，长宽为 450px 和 50px
        new_captcha = Image.new("RGB", (450, 50))
        # 将三份图片按顺序拼接到新的图片上
        new_captcha.paste(part1, (0, 0))
        new_captcha.paste(part2, (150, 0))
        new_captcha.paste(part3, (300, 0))
        # 保存新的图片
        new_captcha.save(self.ImgFile+"/captcha_new.jpg")
    def discernImgSpider(self):
        question,validUrl = self.firstVerify()
        self.imgsortSpider()
        ocr = ddddocr.DdddOcr()
        with open(self.ImgFile+"/captcha_new.jpg", 'rb') as f:
            img_bytes = f.read()
        recognition_result = str(ocr.classification(img_bytes))  # captcha_new.jpg 识别的结果
        print(f'要点选的数字：{question}')
        print(f'识别出的背景数字：{recognition_result}')
        # question = [1, 8, 3, 6]  # 要点击的数字
        # recognition_result = '123564987'
        mapping_table = {
            "0": f"{str(random.randint(15, 35))},{str(random.randint(15, 35))}|",
            "1": f"{str(random.randint(65, 85))},{str(random.randint(15, 35))}|",
            "2": f"{str(random.randint(115, 135))},{str(random.randint(15, 35))}|",
            "3": f"{str(random.randint(15, 35))},{str(random.randint(65, 85))}|",
            "4": f"{str(random.randint(65, 85))},{str(random.randint(65, 85))}|",
            "5": f"{str(random.randint(115, 135))},{str(random.randint(65, 85))}|",
            "6": f"{str(random.randint(15, 35))},{str(random.randint(115, 135))}|",
            "7": f"{str(random.randint(65, 85))},{str(random.randint(115, 135))}|",
            "8": f"{str(random.randint(115, 135))},{str(random.randint(115, 135))}|",
        }
        answer = ""
        for q in question:
            for r in recognition_result:
                if q == int(r):
                    answer += mapping_table[str(recognition_result.index(r))]
        print(answer)
        # answer = '125,120|26,66|20,120|85,12|'
        # url = 'https://s9verify.baixing.com/b6c63b265406596d6ec826637fa2a05d:06f76a707e7fdef49ad5f9f82d5c2f5403572906.1706004717.valid?mobi=n&data=77,25|123,121|130,23|14,32|&callback=jQuery111303584524002624765_1706004715463&_=1706004715464'
        url = 'https://s9verify.baixing.com/b6c63b265406596d6ec826637fa2a05d:06f76a707e7fdef49ad5f9f82d5c2f5403572906.1706004717.valid?mobi=n&data={}'.format(answer)
        url = validUrl#+'&data='+answer
        print(url)
        data = {'data':answer}
        respon = requests.get(url=url,headers=self.headers,data=data,proxies=self.proxy, verify=False)
        respon.encoding=respon.apparent_encoding
        print(respon,respon.text)


if __name__ == '__main__':
    sudoku = sudokuVerify()
    # sudoku.firstVerify() # 获取Cookie和验证码背景
    # sudoku.imgsortSpider()#图片排序
    sudoku.discernImgSpider()#识别图片和点击轨迹

