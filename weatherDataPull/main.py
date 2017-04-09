'''
Created on 4 Apr 2017

@author: David Fottrell 09138773

The purpose of this code is to directly pull JSON data from Open Weather & Dublin Bikes websites and parse it 
directly into a SQL database, instead of sending to a file as is currently the case.

'''
import time
import datetime
import json
import urllib.request
import pymysql.cursors


def main():
    dP = dataScrape()
    dP.timer()
    return


class dataScrape(object):
    '''
    This class will provide similar functionality to main.dataPull(), however we will modify it to redirect the API
    result to the data base rather than to a file.
    
    To simplify matters, we will copy code directly from main.dataPull() where appropriate.  What I'm planning here 
    is sufficiently different to warrant an entirely new class.
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    
    def getWeather(self):
        '''
        Am taking a different approach from previous scraping API because we are handling JSON data directly, I want
        to keep things simple.  The old method may prove just as effective, but I received a victim impact statement 
        after my previous project importing and processing JSON data!!!
        
        Inspiration for this approach came from 
        http://stackoverflow.com/questions/40247392/inserting-json-object-into-mysql-using-python 
        '''
        
            # Database connection phase - Obtained from mypysql library manual https://media.readthedocs.org/pdf/pymysql/latest/pymysql.pdf
        connection = pymysql.connect(host = 'bikeandweather.cnkbtyr1hegq.us-east-1.rds.amazonaws.com',
                                     user = 'admin',
                                     password = 'Conv2017',
                                     db = 'BikeAndWeather',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        
        
        # Openweather API call phase
        url = 'http://api.openweathermap.org/data/2.5/weather?id=7778677&APPID=0b1d40f0f5b1bc4af97416f01400dd72&units=metric'
        wthr = urllib.request.urlopen(url).read()
        data = json.loads(wthr.decode('utf-8'))            
    
    
        # These variables are initiliased outside the for loop to make them available to the cursor.execute function later
        date = data['dt']
        main = ""
        desc = ""
        icon = ""
        temp = data['main']['temp']
        
        '''
            Receiving warnings here; Warning: (1265, "Data truncated for column 'temp' at row 1").
            In the database, it is truncating the value to an integer value only.  Efforts to fix this
            have lead nowhere.  So I have decided to live with this for now!
        
        '''
    
        for i in data['weather']:
            main = i['main']
            desc = i['description']
            icon = i['icon']
    
        print("The current temperature is: ", temp)
    
        try:
            with connection.cursor() as cursor:
                # create new record
                sql = "INSERT INTO BikeAndWeather.Weatherdata (date, main, description, icon, temp) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (date, main, desc, icon, temp))
                
            connection.commit()
            
        finally:
            connection.close() 
        
        ''' Database write phase 
            Note that the date is the database key
        '''
        #for data in wthr_obj["object"]: 
        #    cursor.execute("INSERT webscraper.weather(date, main, description, icon, temp) VALUES (data['dt'],data.weather['main'], data.weather['description'], data.weather['icon'], data.main['temp']);")

        
    def timer(self):
        counter = 0
        '''
        Note - requests should not be more than once every 10 minutes, direction from openweathermap.org
        This timer will be used to prevent excessive calls to the openweathermap API.
        
        168 hrs / week, for 2 weeks = 336 calls, 15 min intervals gives 1344 calls.  Timing function 
        waits 15 mins after triggering the data pull
        '''
        while (counter < 12):        
            gW = dataScrape()
            gW.getWeather()            
            #gW.getBikes()                
            time.sleep(3600)           
            counter += 1    


if __name__ == '__main__':
    main()