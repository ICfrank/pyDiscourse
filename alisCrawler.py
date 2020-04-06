from requests import Session
import json
import requests
import lxml
import re
from scrapy import Selector
from fake_useragent import UserAgent

ua = UserAgent()
user_agent = {'User-agent': ua.random,'Referer': 'https://alisdeals.com/'}
session = Session()
session.head('https://alisdeals.com/deal/DF3D54CD7DCF459')

response = session.post(
    url='https://alisdeals.com/home/catlist',
    data={
        'id': 'c',
        'sub': 'kids'
    },
    headers=user_agent
)

print(response.status_code)
# print(response.text)

response_x = Selector(text=response.text)
item_lists = response_x.xpath("""//div[@class='row']/div[contains(normalize-space(@class), 'store-product d-none')]""")
# print(item_lists)
for item in item_lists:
    link = item.xpath(""".//a/@href""").get('')
    print(link)
    title = item.xpath(""".//span[@class='info']/span[@class='name']/text()""").get('').strip()
    print(title)
    image = item.xpath(""".//a//img[@class='img-fluid']/@src""").get('').strip()
    print(image)
    price = item.xpath(""".//span[@class='info']//span[contains(normalize-space(@class), 'price')]/text()[last()]""").get('').strip()
    price_bef = item.xpath(""".//span[@class='info']/span[contains(normalize-space(@class), 'price')]/span[contains(normalize-space(@class), 'before')]/text()""").get('').strip()
    print(price)
    print(price_bef)
    percent = item.xpath(""".//span[contains(normalize-space(@class), 'flag')]/text()""").re_first('(\d+)[%]?')
    print(percent)

    product = 'https://alisdeals.com/'+link
    r_product = requests.get(product,headers=user_agent)
    # print(r_product.text)
    r_product_x = Selector(text=r_product.text)
    asin = r_product_x.xpath("""//a[@id='linkNotFB']/@href""").re_first('(?:[/dp/]|$)([A-Z0-9]{10})')

    dealid = re.findall("""\"dealid\":\s?\'(\d+)\'""",r_product.text)
    print(dealid)

    session2 = Session()
    if(dealid):
        response2 = session2.post(
            url='https://alisdeals.com/home/claimDeal',
            data={
                "dealid": dealid[0],
                'dataType': 'json'
            },
            headers={
                'Referer': product
            }
        )
        print(response2.text)
        code = json.loads(response2.text)['Message']
        print(code)

        result = {
            'asin':asin,
            'code':code,
            'percent':percent,
            'image':image,
            'price':price,
            'price_old':price_bef,
            'title':title
        }
        print(result)














#
