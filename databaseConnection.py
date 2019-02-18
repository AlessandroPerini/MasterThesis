import pymysql.cursors


class DBConnection:

    def __init__(self):
        self.connected = False
        self.connection = pymysql.connections

    def database_connection(self):
        try:
            conn = pymysql.connect(host='localhost',
                                   user='root',
                                   password='vuota',
                                   db='census',
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)
            self.connection = conn
            self.connected = True
            print('\n Database connected! \n')
        except ValueError as ve:
            print(ve)
            print("Connection problem!")

    def query(self, query):
        if self.connected:
            try:
                with self.connection.cursor() as cursor:
                    sql = query
                    ''' SELECT * FROM censusdata WHERE id=1 '''
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
            except ValueError as ve:
                print(ve)

        else:
            print("Database is not connected")

    def return_connection(self):
        if self.connected:
            return self.connection

    def close_connection(self):
        if self.connected:
            self.connected = False
            self.connection.close()
