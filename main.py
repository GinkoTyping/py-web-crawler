from scraper import Scraper
from db_handler import DBHandler

def main():
    scraper = Scraper(url="https://zu.fang.com/house/a21/")  # 替换为你要抓取的网页URL
    data, images = scraper.scrape_data()

    print(data, images)

    # db_handler = DBHandler(
    #     host="localhost",
    #     user="root",
    #     password="123456",
    #     database="your_database"
    # )
    #
    # db_handler.connect()
    # db_handler.store_data(data)
    # db_handler.store_images(images)
    # db_handler.disconnect()

if __name__ == "__main__":
    main()