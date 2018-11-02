import requests
from bs4 import BeautifulSoup
import redis

def request_daili_list(url,count,headers):
    for i in range(1,count+1):
        page_url = url + str(i)
        res = requests.get(url=page_url,headers=headers)
        yield res.text


def parse_daili(html):
    soup = BeautifulSoup(html,'lxml')
    ip_list = soup.select("[data-title='IP']")
    cotegaries = soup.select("[data-title='类型']")
    ports = soup.select("[data-title='PORT']")
    proxies = []
    for i in range(len(ip_list)):
        proxy = cotegaries[i].get_text().lower() + '://' + ip_list[i].get_text() + ":" + ports[i].get_text()
        proxies.append(proxy)

    return proxies

# 验证代理
def verify_proxeis(proxies,headers):
    avaiable_proxies = []
    print(proxies)
    for proxy in proxies:
        protocol = 'https' if 'https' in proxy else 'http'
        proxys = {protocol: proxy}
        # print(proxy)
        if requests.get(url="https://www.baidu.com",headers=headers,proxies=proxys,timeout=2).status_code == 200:
            print("代理可用:", proxy)
            avaiable_proxies.append(proxy)

    return avaiable_proxies


# 写入redis
def wirte_to_redis(ip):
    r = redis.Redis(host='192.168.10.131', port=6379,db=0,charset='utf-8')
    for i in ip:
        r.lpush('ip',i)

if __name__ == '__main__':
    url = 'https://www.kuaidaili.com/free/inha/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }

    html_pages = request_daili_list(url,10,headers)
    proxies = []
    for page in html_pages:
        proxies += parse_daili(page)
    # print(proxies)
    myip_list = verify_proxeis(proxies,headers)
    wirte_to_redis(myip_list)