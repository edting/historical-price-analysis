import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
from mplfinance.original_flavor import candlestick_ohlc

def plot_candle( ohlc,
                 xlabel = "Date",
                 ylabel = "Price [$]",
                 width = 0.6,
                 colorup = 'green',
                 colordown = 'red',
                 alpha = 0.8,
                 **kwargs ):
    fig, ax = plt.subplots()
    candlestick_ohlc(ax, ohlc.values, width=width, colorup=colorup, colordown=colordown, alpha=alpha, **kwargs)
    date_format = mpl_dates.DateFormatter('%d-%m-%Y')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()
    prettify(xlabel, ylabel, rotate=True)

def plot_line( x,
               y,
               xlabel = "x",
               ylabel = "y",
               horizontal = [],
               **kwargs ):
    if horizontal:
        for value in horizontal:
            plt.axhline(y=value, color='lightgrey', linestyle='dashed')
    plt.plot(x, y, **kwargs)
    prettify(xlabel, ylabel, rotate=True)

def plot_hist( values,
               xlabel = "Values",
               ylabel = "Frequency",
               axisrange = None,
               nbins = 50,
               density = False,
               color = "royalblue",
               alpha = 0.5,
               legend = "",
               **kwargs ):
    plt.hist(values, range=axisrange, bins=nbins, density=density, color=color, alpha=alpha, label=legend, **kwargs)
    prettify(xlabel, ylabel)

def plot_hist2d( x,
                 y,
                 xlabel = "",
                 ylabel = "",
                 zlabel = "",
                 text = False,
                 **kwargs ):
    hist, xbins, ybins, image = plt.hist2d(x, y, **kwargs)
    cbar = plt.colorbar()
    prettify(xlabel, ylabel)
    if zlabel: cbar.set_label(zlabel)
    if text: # show nonzero bin contents on the plot
        ax = plt.gca()
        for i in range(len(ybins)-1):
            for j in range(len(xbins)-1):
                bin_content = int(hist.T[i,j])
                if bin_content == 0: continue
                xloc = xbins[j] + 0.5*(xbins[j+1]-xbins[j])
                yloc = ybins[i] + 0.5*(ybins[j+1]-ybins[j])
                ax.text(xloc, yloc, bin_content, color="w", ha="center", va="center", fontweight="bold")

def prettify( xlabel = "",
              ylabel = "",
              rotate = False ):
    if xlabel: plt.xlabel(xlabel)
    if ylabel: plt.ylabel(ylabel)
    if rotate: plt.xticks(rotation=45, fontsize='small')
    plt.tight_layout()

def save( name,
          show = False ):
    plt.savefig(f"outputs/{name}.png")
    if show: plt.show()
    else: plt.close()
