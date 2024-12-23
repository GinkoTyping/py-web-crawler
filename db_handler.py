import mysql.connector
from mysql.connector import Error
from agent_info import AgentInfo
from house_info import HouseInfo


class DBHandler:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("已连接至 MYSQL")
        except Error as e:
            print(f"错误: '{e}'")

    def store_houses(self, data: list[HouseInfo]):
        cursor = self.connection.cursor()
        for house in data:
            sql_check_query = "SELECT * FROM house_info WHERE no = %s"
            cursor.execute(sql_check_query, (house.no,))
            result = cursor.fetchone()

            if result is None:
                sql_insert_query = """INSERT INTO house_info (no, name, layout, area, location)
                                      VALUES (%s, %s, %s, %s, %s)"""
                record = (house.no, house.name, house.layout, house.area, house.location)
                try:
                    cursor.execute(sql_insert_query, record)

                    self.connection.commit()
                    print(f"储存房源信息成功： '{house.name}'")
                except Error as e:
                    # 如果发生错误，打印错误信息
                    print(f"获取房源信息失败: '{e}'")
            else:
                print(f"重复房源。该房源信息已被获取：{house.name}")

    def store_agents(self, data: dict[str, AgentInfo]):
        cursor = self.connection.cursor()
        for agent in data.values():
            sql_check_query = "SELECT * FROM agent_info WHERE image_path = %s"
            cursor.execute(sql_check_query, (agent.image_path,))
            result = cursor.fetchone()

            if result is None:
                sql_insert_query = """INSERT INTO agent_info (image_path, name, company, main_area)
                                      VALUES (%s, %s, %s, %s)"""
                record = (agent.image_path, agent.name, agent.company, agent.main_area)
                try:
                    cursor.execute(sql_insert_query, record)

                    self.connection.commit()
                    print(f"存储经纪人信息成功： '{agent.name}'")
                except Error as e:
                    # 如果发生错误，打印错误信息
                    print(f"存储经纪人信息失败: '{e}'")
            else:
                print(f"重复数据。该经纪人信息已被获取：{agent.name}")

    def disconnect(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL 连接关闭")
