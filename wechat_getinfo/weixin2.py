#从get_ip.py中爬取1100条ip存放在proxy_ip.text中
#然后再随机从文档中读取IP使用代理
import linecache
import urllib.request
import random
from bs4 import  BeautifulSoup
import urllib.parse
class Spider(object):
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36r)'
        self.headers = {'User-Agent': self.user_agent}

    def start(self,url,n,proxy):
        try:

            httpproxy_handler = urllib.request.ProxyHandler(proxy)
            opener = urllib.request.build_opener(httpproxy_handler)
            request=urllib.request.Request(url,headers=self.headers)
            response = opener.open(request)
            data=response.read()
            datahref=[]
            title_all=[]                    #存放标题
            soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
            links=soup.find_all('div',class_='img-box')
            for link in links:
                datahref.append(link.a['href'])
                # print(link.a['href'])
            file=open('link.text','a')          #链接写到link文档中

            for i in range(0,len(datahref)):
                link_ultimate=datahref[i]
                print(datahref[i])
                name=self.getname(link_ultimate)
                title_all.append(name)
                file.write(name+link_ultimate)
            n=n+1
        except Exception as e:
            print(e)
            # print('ip boom')
        return n
    def getname(self, url):  # 获取每一个公众号的名称
        try:
            request = urllib.request.Request(url, headers=self.headers)
            response = urllib.request.urlopen(request)
            data = response.read()
            soup = BeautifulSoup(data, 'html.parser', from_encoding='utf-8')
            tag = soup.strong
            name = tag.contents[0].replace(" ","").replace("\n",'')         #用replace方法
            # print(tag.contents[0])
            print(name)
            # print(tag.contents)
        except Exception as e:
            print(e)
        return name

    def get_random_ip(self):
        proxy_file = open('proxy_list.text', 'r')
        proxy_list = []
        for line in proxy_file:
            proxy_list.append(line)
        proxy_ip = random.choice(proxy_list)
        proxies = {'http': str(proxy_ip).split('\'')[3]}
        print(proxies)
        return proxies


if __name__=='__main__':
    # title=input("输入要搜索的内容")
    spider = Spider()

    i=1
    while(i<11):
        url='http://weixin.sogou.com/weixin?query=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&type=1&page='+str(i)+'&ie=utf8&p=76331800&dp=1'
        proxy=spider.get_random_ip()
        n=spider.start(url,i,proxy)


