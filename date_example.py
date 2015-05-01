
import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import dateutil.relativedelta as relativedelta
import matplotlib.dates as mdates
from matplotlib import rc

#r = requests.get('http://www.google.com/finance/getprices?i=60&p=2d&f=d,o,h,l,c,v&df=cpct&q=TWTR')

def parse_data(file):

    with open(file) as f:
        
        for _ in range(7):
            next(f)
        time_stamp = f.readline().split(',')[0]
        start_time = datetime.datetime.fromtimestamp(int(time_stamp[1:]))
        
        data = f.read().split()
        data = [row.split(',') for row in data]
        df = pd.DataFrame(data)

        df.drop(0, axis=1, inplace=True)
        df.columns = ['Close', 'High', 'Low', 'Open', 'Volume']

    dates = list()

    current_date = start_time
    for _ in range(len(df)):
        dates.append(current_date)
        current_date += relativedelta.relativedelta(minutes=1)
        

    df['date_time'] = dates
    return df

def plot_graph(df):
    fig, ax = plt.subplots(figsize=(15,10))

    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 16}

    rc('font', **font)

    stock_price = list(df['Close'])
    dates = list(df['date_time'])

    fmt_major = mdates.DateFormatter('%H:%M')
    loc_major = mdates.HourLocator(byhour=range(24), interval=2)

    ax.plot(dates, stock_price, linestyle='-', linewidth = 2, markersize=1, label='Twitter stock price')

    ax.xaxis.set_major_locator(loc_major)
    ax.xaxis.set_major_formatter(fmt_major)

    ax.set_ylabel('Price($)')
    plt.title('Twitter Stock Prices - 28 Apr 2015')

    plt.savefig('stock_trend.png')
    plt.show()


df = parse_data('stock_price_data.txt')
plot_graph(df)
