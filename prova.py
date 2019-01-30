import pymysql.cursors


class DBConnection(object):

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
            print('\n Connessione OK! \n')
        except:
            print("Problema di connessione")

    def query(self, query):
        if self.connected:
            try:
                with self.connection.cursor() as cursor:
                    sql = query
                    ''' SELECT * FROM censusdata WHERE id=1 '''
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
            finally:
                self.connection.close()
        else:
            print("Connessione non aperta")
