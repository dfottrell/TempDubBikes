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
import pymysql


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
        
        # Openweather API call phase
        #url = 'http://api.openweathermap.org/data/2.5/weather?id=7778677&APPID=0b1d40f0f5b1bc4af97416f01400dd72&units=metric'
        #urllib.request.urlopen(url).read()
        #wthr = urllib.request.urlopen(url).read()
        #wthr_obj = json.loads(wthr.decode('utf-8'))
        
    
        # Database connection phase
        # Looks like local IP needs to be added t AMAZON security group for this to work
        con = pymysql.connect(host = 'bikeandweather.cnkbtyr1hegq.us-east-1.rds.amazonaws.com:3306', user = 'admin', passwd = 'Conv2017', db = 'rdsDataBase')
        cursor = con.cursor()
        results = cursor.fetchone()
        
        if results:
            print("The database is connected properly")
        else:
            print("Database connection failed")
        
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
        while (counter < 1):        
            gW = dataScrape()
            gW.getWeather()            
            #gW.getBikes()                
            time.sleep(3)           
            counter += 1    


if __name__ == '__main__':
    main()