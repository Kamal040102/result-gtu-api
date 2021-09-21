from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time

app = Flask(__name__)

@app.route("/")
def getResult():
    page = requests.get('https://www.gtu.ac.in/result.aspx').text
    soup = BeautifulSoup(page, 'lxml')
    cards = soup.find_all('div', class_='event-list')
    result_int = {}
    key = 0
    for card in cards:
        title = card.find('h3', class_='Content').text
        date = card.find('div', class_='date-in').text
        # print(f'The {title}has been announced on date {date}.')
        value = f'The {title} has been announced on date {date}.'
        result_int[key] = value
        key += 1

    fd = open('result.json', 'r')
    data = fd.read()
    fd.close()
    
    data_json = json.loads(data)
    
    first_int = result_int[0]
    first_data = data_json['0']
    curr_time = datetime.today().strftime('%d/%m/%Y')
    yester_date = str(int(datetime.today().strftime('%d')) - 1)
    today_date = datetime.today().strftime('%d')
    curr_month = time.ctime().split()[1]
    
    
    if first_int == first_data:
        give = "No new result has been declared as of "
        return render_template('index.html',give=give, curr_time=curr_time, data_json=data_json, yester_date=yester_date, today_date=today_date, curr_month=curr_month)
    else:
        give = "Results declared as of "
        result_json = json.dumps(result_int)
        fd = open('result.json', 'w')
        fd.write(result_json)
        fd.close()
        return render_template('index.html',give=give, curr_time=curr_time, data_json=data_json)

if __name__ == '__main__':
    app.run(debug=True)