from neuralintents import GenericAssistant
import matplotlib.pyplot as plt
import pandas as pd 
import pandas_datareader as web
import mplfinance as mpf
import nltk
import pickle
import sys
#import datetime as dt
#hellonltk.download('omw-1.4')
#make intents.json file

#creating portfolio
#portfolio = {'AAPL':20, 'TSLA': 5, 'GS':10}
#with open ('portfolio.pkl', 'wb') as f:
#    pickle.dump(portfolio, f)

#opening portfolio
portfolio = {'AAPL':20, 'TSLA': 5, 'GS':10}
with open ('portfolio.pkl', 'rb') as f:
    portfolio = pickle.load(f)
#print(portfolio)
def greeting():
    print ("Hello")
def save_portfolio():
    with open ('portfolio.pkl', 'wb') as f:
        pickle.dump(portfolio, f)
#Add to portfolio
def add_portfolio():
    ticker = input("Which stock do you want to add:")
    amount = input ("How many shares do you wnat to add:")

    if ticker in portfolio.keys():
        portfolio[ticker] += amount
    else:
        portfolio[ticker] = amount
#Sell Stock
def remove_portfolio():
    ticker = input("Which stock do you want to sell:")
    amount = input ("How many shares do you wnat to sell:")
    if ticker in portfolio.keys():
        if amount <= portfolio[ticker]:
            portfolio[ticker] -= amount
            save_portfolio()
        else:
            print("You don't have enough shares!")
    else:
        print(f"You don't own any shares of  {ticker}")
#show portfolio
def show_portfolio():
    print("Your portfolio:")
    for ticker in portfolio.keys():
        print("You won {portfolio[ticket]} shares of {ticker}")

def portfolio_worth():
    sum=0
    for ticker in portfolio.keys():
        data=web.DataReader(ticker, 'yahoo')
        price = data['close'].iloc[-1]
        sum += price
    print(f"Your portfolio is worth {sum} USD")    

def portfolio_gains():
    starting_date= input ("Enter a date for comparison (YYYY-MM-DD):")
    sum_now = 0
    sum_then = 0
    try:
        for ticker in portfolio.keys():
            data = web.DataReader(ticker, 'yahoo')
            price_now = data['Close'].iloc[-1]
            price_then = data.loc[data.inderx == starting_date]['Close'].values[0]
            sum_now += price_now
            sum_then += price_then
        print(f"Relative Gains :{((sum_now-sum_then)/sum_then) * 100}%")
        print(f"Absolute Gains :{sum_now-sum_then} USD")
    except IndexError:
        print("There was no trading on this day")
#ploting
def plot_chart():
    ticker = input("Choose a ticker symbol: ")
    starting_string = input ("Choose a starting date (YYYY-MM-DD): ")

    plt.style.use('dark_background')

    start = dt.datetime.strptime(starting_string, "%d/%m/%Y")
    end = dt.datetime.now()

    data=web.DataReader(ticker, 'yahoo', start, end)

    colors= mpf.make_marketcolors(up='#00ff00', wick='inherit', edge='inherit', volume='in')
    mpf_style = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=colors)       
    mpf.plt(data, type='candle', style = mpf_style, volume=True) 
def bye():
    print("Goodbye")
    sys.exit(0)

mappings = {
    'greetings':greeting,
    'plot-chart':plot_chart,
    'add_portfolio': add_portfolio,
    'remove_portfolio': remove_portfolio,
    'show_portfolio': show_portfolio,
    'portfolio_worth': portfolio_worth,
    'portfolio_gains': portfolio_gains,
    'bye': bye
}

assistant = GenericAssistant('intents.json', mappings, "financial_assistant_model")

assistant.train_model()
assistant.save_model()

while True:
    message=input("")
    assistant.request(message)