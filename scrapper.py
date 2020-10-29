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

    yesterday = date.today() - timedelta(days=1)
    print("Date:", yesterday)

    df = pd.read_csv("https://health-infobase.canada.ca/src/data/covidLive/covid19-download.csv",usecols=col_list)
    df['date_filter'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df_filtered = df[(df['date_filter'] == yesterday.strftime('%Y-%m-%d'))]
    #df_filtered.to_csv("covidData.csv")
    df_filtered.to_json (r'covidData.json')

    data = open("covidData.json", "r").read()

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

