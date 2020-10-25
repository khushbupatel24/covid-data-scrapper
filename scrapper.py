import csv
import json
import pandas as pd
from datetime import date, timedelta
import datetime
from  urllib.request  import urlretrieve as retrieve

def filter():
    col_list = ["prname", "pruid","date","numconf","numdeaths","numtotal","numtested","numrecover","percentrecover","numtoday","percentoday","ratetotal","ratedeaths","percentactive","numdeathstoday","percentdeath","percentactive"]
    
    yesterday = date.today() - timedelta(days=1)
    print("Date:", yesterday)

    df = pd.read_csv("https://health-infobase.canada.ca/src/data/covidLive/covid19-download.csv",usecols=col_list)
    df['date_filter'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df_filtered = df[(df['date_filter'] == yesterday.strftime('%Y-%m-%d'))]
    #df_filtered.to_csv("covidData.csv")
    df_filtered.to_json (r'covidData.json')

filter()

# def j():
   
#     df = pd.read_csv('covidData.csv')
#     df.to_json (r'a.json')
# j()
