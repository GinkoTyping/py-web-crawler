import mysql.connector
from mysql.connector import Error

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
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error: '{e}' occurred")

    def store_data(self, data):
        cursor = self.connection.cursor()
        sql_insert_query = """INSERT INTO pages (title, description)
                              VALUES (%s, %s)"""
        record = (data['title'], data['description'])
        try:
            cursor.execute(sql_insert_query, record)
            self.connection.commit()
            print("Data inserted successfully")
        except Error as e:
            print(f"Error: '{e}' occurred")

    def store_images(self, images):
        cursor = self.connection.cursor()
        for image_path in images:
            with open(image_path, 'rb') as file:
                binary_data = file.read()

            sql_insert_query = """INSERT INTO images (image_data)
                                  VALUES (%s)"""
            record = (binary_data,)
            try:
                cursor.execute(sql_insert_query, record)
                self.connection.commit()
                print(f"Image {image_path} inserted successfully")
            except Error as e:
                print(f"Error: '{e}' occurred")

    def disconnect(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")