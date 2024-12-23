from scraper import Scraper
from db_handler import DBHandler


def main():
    scraper = Scraper(url="https://zu.fang.com/house/a21/")  # 替换为你要抓取的网页URL
    houses_info = scraper.scrape_data()

    print(houses_info)

    db_handler = DBHandler(
        host="localhost",
        user="root",
        password="123456",
        database="rental_info"
    )

    db_handler.connect()
    db_handler.store_house(houses_info)

    db_handler.disconnect()


if __name__ == "__main__":
    main()
