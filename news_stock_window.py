import tkinter as tk
from tkinter import Tk, ttk, Label, Button, StringVar, IntVar, Text, Scrollbar, Listbox, Entry
import newspaper
from newspaper import Article
from yahoo_fin import stock_info as si
import time
import datetime
from datetime import date, timedelta
import pandas as pd
from matplotlib.figure import Figure
import numpy as np
import matplotlib
import matplotlib.dates as mdates
import pandas_datareader as web
from mpl_finance import candlestick_ohlc
matplotlib.use("TKAgg")
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class GUI:

    def __init__(self, master):

        self.start_date = str(date.today() - timedelta(days = 480))
        self.end_date = str(date.today())

        self.master = master
        master.title("News summary")

        self.time_and_date = Label(master, text = 'Today is %s' % time.ctime())
        self.time_and_date.pack(ipadx = 10, expand=1)

        self.stock_name = Entry(master)
        self.stock_name.pack(ipadx = 10, expand=1)
        self.ticker = ''
        self.sp500 = '^GSPC'
        self.crude = 'CL'
        self.nasdaq = '^IXIC'

        self.stock_button = Button(master, text='Run', command=self.getStockName, width = 20, bd = 5, font = 'black', relief = 'groove', state = 'active')
        self.stock_button.pack(expand=1)


        self.sp_500_label = Label(master, text = "SP 500 Price: %s" % round(si.get_live_price(self.sp500), 2))
        self.sp_500_label.pack(expand=1)

        self.nasdaq_label = Label(master, text = "NASDAQ Price: %s" % round(si.get_live_price(self.nasdaq), 2))
        self.nasdaq_label.pack(expand=1)

        self.crude_label = Label(master, text = "Crude Price: %s" % round(si.get_live_price(self.crude), 2))
        self.crude_label.pack(expand=1)

        self.news_descrip = Label(master, text = 'Choose your news source below:')
        self.news_descrip.pack(expand=1)

        self.news_names = StringVar()
        self.news = ttk.Combobox(root, textvariable=self.news_names)
        self.news['values'] = ("BBC", "Reuters", "New York Times", "CNN", "Fast Company")

        self.news.pack(expand=1)
        self.news.current(0)

        self.n_articles_descrip = Label(master, text = 'Choose the number of articles you would like to read below:')
        self.n_articles_descrip.pack(expand=1)

        self.number_names = IntVar()
        self.number = ttk.Combobox(root, textvariable=self.number_names)
        self.number['values'] = (1, 2, 3, 4, 5, 6, 7, 8)

        self.number.current(0)
        self.number.pack(expand=1)

        self.greet_button = Button(master, text='Run', command=self.play, width = 30, bd = 5, font = 'black', relief = 'groove', state = 'active')
        self.greet_button.pack(ipadx = 10, pady = 1, expand=1)

        self.outputtext = Text(master)
        self.outputtext.pack(pady = 1, fill='both', expand=1)

    def play(self):

        test = self.news.get()
        number = self.number.get()
        n_articles = int(number)

        if(test == 'BBC'):
            url = 'https://www.bbc.com'
        elif(test == 'Reuters'):
            url = 'https://www.reuters.com'
        elif(test == 'CNN'):
            url = 'https://www.cnn.com'
        elif(test == 'Fast Company'):
            url = 'https://www.fastcompany.com'            
        else:
            url = 'https://www.nytimes.com'

        titles = ' '
        paper = newspaper.build(url)
        for article in paper.articles[:n_articles]:
            article.download()
            article.parse()
            article.nlp()
            titles += 'Title: ' + article.title + '\n' + '\n ' + article.summary + '\n' + '----------------------' + '\n'


        self.outputtext.delete('0.0', '900000.0')
        self.outputtext.insert('0.0', titles)

    def getStockName(self):
        name = self.stock_name.get()
        self.ticker = name

        df = web.DataReader(self.ticker, 'yahoo', self.start_date, self.end_date)
        df = df[['Open', 'High', 'Low', 'Close']]
        df.reset_index(inplace=True)
        df['Date'] = df['Date'].map(mdates.date2num)
        
        fig = plt.figure(figsize=(10, 8))
        ax = plt.subplot()
        candlestick_ohlc(ax, df.values, width=1.5, colorup='g', colordown='r')
        ax.xaxis_date()
        plt.title(self.ticker)
        ax.grid(True)
        plt.show()  

root = Tk()
root.option_add('*TCombobox*Listbox.selectBackground', 'grey') # change highlight color
root.geometry('1000x800')
my_gui = GUI(root)
root.mainloop()