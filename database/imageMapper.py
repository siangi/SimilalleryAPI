import mysql.connector
import database.connection as connection
import models.imageData as imageModels

class imageMapper:
    def __init__(self) -> None:
        self._dbConnection =  mysql.connector.connect(host=connection.host, username=connection.username, password=connection.password, database="scheme_test_similallery")

    def searchRecords(self, query: str) -> tuple:
        cursor = self._dbConnection.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data

    

        