import requests
import base64
import csv
import json
import pandas as pd
from datetime import date, timedelta
import datetime
from  urllib.request  import urlretrieve as retrieve

def filter():
    col_list = ["prname", "pruid","date","numconf","numdeaths","numtotal","numtested","numrecover","percentrecover","numtoday","percentoday","ratetotal","ratedeaths","percentactive","numdeathstoday","percentdeath","percentactive"]
    col1=["prname","numdeaths"] # columns for death chart
    col2=["prname","numtested"] # columns for tested chart
    col3=["prname","numrecover"] # columns for recovered chart
    col4=["prname","numtotal"]  # columns for total chart
    col5=["prname","percentactive"] #columns for active percentage
    yesterday = date.today() - timedelta(days=1)
    print("Date:", yesterday)

    df = pd.read_csv("https://health-infobase.canada.ca/src/data/covidLive/covid19-download.csv",usecols=col_list)
    df['date_filter'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df_filtered = df[(df['date_filter'] == yesterday.strftime('%Y-%m-%d'))]
    
    d=df_filtered.filter(col1) #filter by columns
    d=d.rename(columns={"prname": "province", "numdeaths": "number of deaths"}) #renaming columns
    d=d.set_index("province") #changing keys
    d.to_json (r'Death.json')

    d=df_filtered.filter(col2)
    d=d.rename(columns={"prname": "province", "numtested": "people tested"})
    d=d.set_index("province")
    d.to_json (r'Tested.json') # file for number of people tested 

    
    d=df_filtered.filter(col3)
    d=d.rename(columns={"prname": "province", "numrecover": "recovered"})
    d=d.set_index("province")
    d.to_json (r'recovered.json') # file for total recovered cases

    d=df_filtered.filter(col4)
    d=d.rename(columns={"prname": "province", "numtotal": "total cases"})
    d=d.set_index("province")
    d.to_json (r'total.json') # file for total death cases

    d=df_filtered.filter(col5)
    d=d.rename(columns={"prname": "province", "percentactive": "active percentage"})
    d=d.set_index("province")
    d.to_json (r'active.json') # file for active percentage cases
   

    data = open("Death.json", "r").read()

    token = "385b412e10720f3ea07bef43cf810bde19e1d828"
    owner = 'khushbupatel24'
    repo = 'covid-data'
    path = 'deathRate.json'

    url = 'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    r = requests.get(f'https://api.github.com/repos/{owner}/{repo}/contents/{path}')
    print(r.json()['sha'])

    r = requests.put(
        f'https://api.github.com/repos/{owner}/{repo}/contents/{path}',
        headers = {
            'Authorization': f'Token {token}'
        },
        json = {
            "message": "add new file",
            "content": base64.b64encode(data.encode()).decode(),
            "branch": "main",
            "sha": r.json()['sha']
        }
    )
    print(r.status_code)
    print(r.json())

filter()

