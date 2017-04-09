'''
Created on 7 Apr 2017

@author: User
'''
import pymysql

connection = pymysql.connect(host = '127.0.0.1',
                            user = 'root',
                            db = 'test_connector',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
        
try:
    with connection.cursor() as cursor:
        # create new record
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
                
    connection.commit()
            
    with connection.cursor() as cursor:
        # read a single record
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close() 
