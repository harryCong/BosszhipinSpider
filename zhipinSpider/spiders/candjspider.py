import requests
from lxml import etree
from selenium import webdriver
import redis
url = "https://www.zhipin.com/"

def creat_url():
    # headers = {'user_agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    driver = webdriver.Chrome()

    driver.get(url=url)

    html_tree = etree.HTML(driver.page_source)

    city_list = html_tree.xpath("//div[@class='dorpdown-city']//li/@data-val")

    job_list = html_tree.xpath("//div[@class='job-menu']//a/@href")
    # print(city_list)
    job_code = []
    for job in job_list:
        job_code.append(job.split("-")[-1])
    # 把城市代号和岗位代号一起拼接成一个url
    for city in city_list:
        for job in job_code:
            print("https://www.zhipin.com/c" + city +"-" + job)


def write_to_redis(res):
    r = redis.StrictRedis(host='192.168.10.131', port=6379, db=0, charset='utf-8')
    for i in res:
        r.lpush('zhipin:start_urls',i)


if __name__ == '__main__':
    write_to_redis(create_url())
# creat_url()