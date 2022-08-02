import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac
import pandas as pd
from models import Orders
from peewee import *
from urllib import request
import ast
from bs4 import BeautifulSoup
import datetime

date = datetime.datetime.now().strftime('%d/%m/%Y')

def get_usd_course():
    with request.urlopen(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}') as resp:
        data = resp.read()
        soup = BeautifulSoup(data, 'xml')
        items = soup.find_all('Valute', attrs={'ID': 'R01235'})
        for item in items:
            text = item.text[17:]
            text = text.replace(',', '.')
            # print(text)
        return float(text)

USD = get_usd_course()



def gsheet2df(spreadsheet_name):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials_path = './tz-poject-94f3945393e2.json'
    
    credentials = sac.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(credentials)
    
    sheet = client.open(spreadsheet_name).get_worksheet(0).get_all_values()
    df =  pd.DataFrame.from_dict(sheet)

    return sheet


for row in gsheet2df('tz-test')[1:]:
    rub_price = int(row[2]) * USD
    
    Orders.create(
        order_number = int(row[1]),
        price_dollar = int(row[2]),
        price_rub = rub_price,
        delivery_time = row[3]
    )
    print('Done!!!')

