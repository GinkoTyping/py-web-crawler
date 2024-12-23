import requests
from lxml import html
from PIL import Image
from io import BytesIO
from house_info import HouseInfo
from agent_info import AgentInfo
from urllib.parse import urlparse
import os


class Scraper:
    def __init__(self, url):
        self.url = url
        self.agents_urls: dict[str, int] = {}

    def set_host(self, host):
        self.house_host = host

    def scrape_house_info(self):
        response = requests.get(self.url)
        self.set_host(response.url)
        tree = html.fromstring(response.content)

        cards = tree.xpath('//div[@class="houseList"]/dl/dd')
        houses_info = []
        for card in cards:
            no = card.xpath('.//p[@class="title"]/a/@href')[0] + 'l'
            name = card.xpath('.//p[@class="title"]/a/text()')[0]
            layout = card.xpath('.//p[2]')[0].text_content().split('|')[1]
            area = card.xpath('.//p[2]')[0].text_content().split('|')[2]
            location = card.xpath('.//p[3]')[0].text_content()

            house_info = HouseInfo(no, name, layout, area, location)
            houses_info.append(house_info)

            print(f"爬取嵌套的网页中...获取到了房源'{name}'的数据")

        return houses_info

    def scrape_all_agent_info_by_houses(self, houses_data: list[HouseInfo]) -> dict[str, AgentInfo]:
        if not os.path.exists('images/agent'):
            os.makedirs('images/agent')
        agents_info: dict[str, AgentInfo] = {}
        for house_data in houses_data:
            agent_info = self.scrape_agent_info(house_data.no)
            if agent_info is not None and agent_info.image_path not in agents_info:
                agents_info[agent_info.image_path] = agent_info

        return agents_info

    def scrape_agent_info(self, house_no) -> AgentInfo | None:
        url = self.house_host + house_no
        response = requests.get(url)
        tree = html.fromstring(response.content)

        if len(tree.xpath('//div[@class="broker_zf "]')) == 0:
            return None
        else:
            card = tree.xpath('//div[@class="broker_zf "]')[0]

            company = card.xpath('./div[@class="broker_info_n"]/div[2]/span/text()')[0]

            agent_url = 'https:' + card.xpath('./div[@class="broker_img_n"]/a/@href')[0]

            if agent_url not in self.agents_urls:
                self.agents_urls[agent_url] = 1
                agent_response = requests.get(agent_url)
                agent_tree = html.fromstring(agent_response.content.decode('utf-8'))
                agent_card = agent_tree.xpath('//div[@class="conltop clearfix"]')[0]
                agent_card_person = agent_card.xpath('./ul[@class="person"]')[0]

                name = agent_card_person.xpath('./li[@class="name"]/b/text()')[0]
                main_area = agent_card_person.xpath('./li[@class="w60"]/span/a/text()')[0]

                image_url = agent_card.xpath('./img/@src')[0]
                if not image_url.startswith('https:'):
                    image_url = 'https:' + image_url
                image_data = requests.get(image_url).content
                image = Image.open(BytesIO(image_data))

                image_no = urlparse(image_url).path.split('/').pop()
                image_path = os.path.join('images', 'agent', f'{name}_{image_no}')
                image.save(image_path)

                agent_info = AgentInfo(name, company, main_area, image_path)

                print(f"爬取嵌套的网页中...获取到了经纪人'{name}'的数据")

                return agent_info
            else:
                print(f"检测到重复的经纪人的数据，将跳过")
                return None
