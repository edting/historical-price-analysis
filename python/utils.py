import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
from mplfinance.original_flavor import candlestick_ohlc

def plot_candle(ohlc, width=0.6, colorup='green', colordown='red', alpha=0.8, xlabel="Date", ylabel="Price [$]"):
    fig, ax = plt.subplots()
    candlestick_ohlc(ax, ohlc.values, width=width, colorup=colorup, colordown=colordown, alpha=alpha)
    date_format = mpl_dates.DateFormatter('%d-%m-%Y')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()
    prettify(xlabel, ylabel, rotate=True)

def plot_line(x, y, xlabel="x", ylabel="y", horizontal=[]):
    if horizontal:
        for value in horizontal:
            plt.axhline(y=value, color='lightgrey', linestyle='dashed')
    plt.plot(x, y)
    prettify(xlabel, ylabel, rotate=True)

def plot_hist(values, axisrange=None, nbins=50, density=False, color="royalblue", alpha=0.5, xlabel="Values", ylabel="Frequency", legend=""):
    plt.hist(values, range=axisrange, bins=nbins, density=density, color=color, alpha=alpha, label=legend)
    prettify(xlabel, ylabel)

def prettify(xlabel="", ylabel="", rotate=False):
    if xlabel: plt.xlabel(xlabel)
    if ylabel: plt.ylabel(ylabel)
    if rotate: plt.xticks(rotation=45, fontsize='small')
    plt.tight_layout()

def save(name, show=False):
    plt.savefig(f"outputs/{name}.png")
    if show: plt.show()
    else: plt.close()
