import os.path
import shutil

from scraper import Scraper
from db_handler import DBHandler


def main():
    images_dir = 'images/agent'
    urls = [
        "https://zu.fang.com",
        "https://zu.fang.com/house/h316",
    ]
    print("""请选择房源信息的排序方式：
    1. 默认排序（爬取速度快）
    2. 按发布时间排序（爬取速度慢）
    3. 清空爬取数据（爬取数据仅供学习使用，事后将删除）""")
    choice = input("请输入序号：")
    if choice.isdigit():
        db_handler = DBHandler(
            host="localhost",
            user="root",
            password="123456",
            database="rental_info"
        )
        db_handler.connect()

        if 3 == int(choice):
            db_handler.clear()
            if os.path.exists(images_dir):
                shutil.rmtree(images_dir)
        elif 1 <= int(choice) <= len(urls):
            selected_url = urls[int(choice) - 1]
            scraper = Scraper(url=selected_url, images_dir=images_dir)  # 替换为你要抓取的网页URL
            houses_info = scraper.scrape_house_info()
            agents_info = scraper.scrape_all_agent_info_by_houses(houses_info)

            db_handler.store_houses(houses_info)
            db_handler.store_agents(agents_info)

            print(f"爬取完成，经纪人的照片请查看目录：'{images_dir}'")
        else:
            print('输入错误')

        db_handler.disconnect()

    else:
        print('输入错误')


if __name__ == "__main__":
    main()
