import mysql.connector
from mysql.connector import Error

class SqlManager():

    conn = None 

    def __init__(self, host, database, user, password):

        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def connect(self):
        """ Connect to MySQL database """
        try:
            self.conn = mysql.connector.connect(host=self.host,
                                        database= self.database,
                                        user=self.user,
                                        password=self.password)
            if self.conn.is_connected():
                print('Connected to MySQL database')
    
        except Error as e:
            print(e)
    
    def close_connection(self):
        if self.conn is not None and self.conn.is_connected():
                self.conn.close()
                print('Connection closed to MySQL database')

    def upload_to_db(self, df, tablename, exist_type):
        """
        Uploads data to Mysql database
        """
        try: 
            if self.conn.is_connected():
                print('Upload to MySQL database')
                df.to_sql(tablename, self.conn, if_exists = exist_type)

        except Error as e:
            print(e)
        
        finally: 
            self.close_connection()
            

        
    
