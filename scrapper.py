import requests
import base64
import csv
import json
import pandas as pd
from datetime import date, timedelta
import datetime
from  urllib.request  import urlretrieve as retrieve

def uploadDataOnGit(file):
    token = "385b412e10720f3ea07bef43cf810bde19e1d828"
    owner = 'khushbupatel24'
    repo = 'covid-data'

    data = open(file, "r").read()
    path = 'data/' + file

    url = 'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    r = requests.get(f'https://api.github.com/repos/{owner}/{repo}/contents/{path}')
    print(r.status_code)

    if r.status_code != 200 :
        r = requests.put(
            f'https://api.github.com/repos/{owner}/{repo}/contents/{path}',
            headers = {
                'Authorization': f'Token {token}'
            },
            json = {
                "message": "add new file",
                "content": base64.b64encode(data.encode()).decode(),
                "branch": "main",
            }
        )
        print(r.json())
    else:
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


def filter():
    col_list = ["prname", "pruid","date","numconf","numdeaths","numtotal","numtested","numrecover","percentrecover","numtoday","percentoday","ratetotal","ratedeaths","numactive","percentactive","numdeathstoday","percentdeath"]
    col1=["prname","numdeaths"] # columns for death chart
    col2=["prname","numtested"] # columns for tested chart
    col3=["prname","numrecover"] # columns for recovered chart
    col4=["prname","numtotal"]  # columns for total chart
    col5=["prname","percentactive"] #columns for active percentage
    col6=["prname","numconf"]#column for confirmed cases
    col7=["prname","numactive"] #column for active cases number
    col8=["prname","numdeaths","numrecover","numtotal","numconf","numactive","numtested","percentactive"]#for table
    yesterday = date.today() - timedelta(days=1)
    print("Date:", yesterday)

    df = pd.read_csv("https://health-infobase.canada.ca/src/data/covidLive/covid19-download.csv",usecols=col_list)
    df['date_filter'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df_filtered = df[(df['date_filter'] == yesterday.strftime('%Y-%m-%d'))]

    d=df_filtered.filter(col1) #filter by columns
    d=d.rename(columns={"prname": "province", "numdeaths": "number of deaths"}) #renaming columns
    d=d.set_index("province") #changing keys
    d.to_json (r'deathRate.json')
    uploadDataOnGit('deathRate.json')

    d=df_filtered.filter(col2)
    d=d.rename(columns={"prname": "province", "numtested": "people tested"})
    d=d.set_index("province")
    d.to_json (r'Tested.json') # file for number of people tested 
    uploadDataOnGit('Tested.json')

    d=df_filtered.filter(col3)
    d=d.rename(columns={"prname": "province", "numrecover": "recovered"})
    d=d.set_index("province")
    d.to_json (r'recovered.json') # file for total recovered cases
    uploadDataOnGit('recovered.json')

    d=df_filtered.filter(col4)
    d=d.rename(columns={"prname": "province", "numtotal": "total cases"})
    d=d.set_index("province")
    d.to_json (r'total.json') # file for total death cases
    uploadDataOnGit('total.json')

    d=df_filtered.filter(col5)
    d=d.rename(columns={"prname": "province", "percentactive": "active percentage"})
    d=d.set_index("province")
    d.to_json (r'active.json') # file for active percentage cases
    uploadDataOnGit('active.json')

    d=df_filtered.filter(col6)
    d=d.rename(columns={"prname": "province", "numconf": "confirmed cases"})
    d=d.set_index("province")
    d.to_json (r'confirmed.json') # file for confirmed cases
    uploadDataOnGit('confirmed.json')

    d=df_filtered.filter(col7)
    d=d.rename(columns={"prname": "province", "numactive": "active cases"})
    d=d.set_index("province")
    d.to_json (r'activenum.json') # file for active cases in number
    uploadDataOnGit('activenum.json')

    d=df_filtered.filter(col8)
    d=d.rename(columns={"prname": "province","numdeaths": "number of deaths","numrecover": "recovered","numtotal": "total cases","numconf": "confirmed cases","numactive": "active cases","numtested": "people tested","percentactive": "active percentage"})
    d=d.set_index("province")
    d.to_json (r'table.json') # file for table
    uploadDataOnGit('table.json')

filter()

