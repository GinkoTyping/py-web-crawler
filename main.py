from scraper import Scraper
from db_handler import DBHandler


def main():
    house_host = "https://zu.fang.com"
    urls = [
        "https://zu.fang.com",
        "https://zu.fang.com/house/h316/",
    ]
    print("""请选择房源信息的排序方式：
    1. 默认排序
    2. 按发布时间排序""")
    choice = input("请输入序号：")
    if choice.isdigit() and 1 <= int(choice) <= len(urls):
        selected_url = urls[int(choice) - 1]
        scraper = Scraper(url=selected_url)  # 替换为你要抓取的网页URL
        houses_info = scraper.scrape_house_info()
        agents_info = scraper.scrape_all_agent_info_by_houses(houses_info)

        db_handler = DBHandler(
            host="localhost",
            user="root",
            password="123456",
            database="rental_info"
        )

        db_handler.connect()
        db_handler.store_houses(houses_info)
        db_handler.store_agents(agents_info)


        db_handler.disconnect()


if __name__ == "__main__":
    main()
