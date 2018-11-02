import requests
from lxml import etree
from selenium import webdriver

url = 'https://www.zhipin.com/'

def create_url():
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    # }
    broswer = webdriver.Chrome()

    broswer.get(url)
    # r = requests.get(url=url,headers=headers)

    html = etree.HTML(broswer.page_source)
    city_list = html.xpath('//div[@class="dorpdown-city"]//li/@data-val')
    job_list = html.xpath('//div[@class="job-menu"]//a/@href')
    print(city_list)
    print(job_list)
    job_code = []
    for job in job_list:
        job_code.append(job.split('-')[-1])

    for city in city_list:
        for job in job_code:
            yield "https://www.zhipin/com/c" + city + "-" + job

create_url()