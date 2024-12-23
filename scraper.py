import requests
from lxml import html
from PIL import Image
from io import BytesIO
from house_info import HouseInfo
import os


class Scraper:
    def __init__(self, url):
        self.url = url

    def scrape_data(self):
        response = requests.get(self.url)
        tree = html.fromstring(response.content)

        cards = tree.xpath('//div[@class="houseList"]/dl/dd')
        houses_info = []
        for card in cards:
            no = card.xpath('.//p[@class="title"]/a/@href')[0]
            name = card.xpath('.//p[@class="title"]/a/text()')[0]
            layout = card.xpath('.//p[2]')[0].text_content().split('|')[1]
            area = card.xpath('.//p[2]')[0].text_content().split('|')[2]
            location = card.xpath('.//p[3]')[0].text_content()

            house_info = HouseInfo(no, name, layout, area, location)
            houses_info.append(house_info)

        return houses_info
