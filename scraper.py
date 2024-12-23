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
        for card in cards:
            name = card.xpath('.//p[@class="title"]/a/text()')[0]
            layout = card.xpath('.//p[2]/span[1]')[0]
            area = card.xpath('.//p[2]/span[2]')[0]
            test = card.xpath('.//p[3]/a/span')
            location = ''
            for location_level in card.xpath('.//p[3]/a/span'):
                location += location_level.xpath('text()')[0] + '-'


        title = tree.xpath('//title/text()')[0]
        description = tree.xpath('//meta[@name="description"]/@content')[0]

        # 示例图片URL提取，替换为实际的XPath表达式
        image_urls = [img.xpath('@src')[0] for img in tree.xpath('//img')]

        data = {
            'title': title,
            'description': description
        }

        images = []
        for image_url in image_urls:
            image_data = requests.get(image_url).content
            image = Image.open(BytesIO(image_data))
            image_path = os.path.join('images', f'{hash(image_url)}.jpg')
            image.save(image_path)
            images.append(image_path)

        return data, images