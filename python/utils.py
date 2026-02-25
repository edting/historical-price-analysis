import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import mplfinance as mpf
from mplfinance.original_flavor import candlestick_ohlc

def set_plot_style(style='fast'):
    """
    The full list of possible customisations can be found here:
    https://matplotlib.org/stable/users/explain/customizing.html#the-default-matplotlibrc-file
    """
    mpl.style.use(style)
    mpl.rcParams['grid.linestyle'] = '--'
    mpl.rcParams['figure.figsize'] = (8,6)
    mpl.rcParams['figure.dpi'] = 90
    mpl.rcParams['axes.edgecolor'] = 'black'
    mpl.rcParams['axes.labelsize'] = 14
    mpl.rcParams['font.size'] = 11

def plot_candle( ohlc,
                 xlabel = "Date",
                 ylabel = "Price [$]",
                 **kwargs ):
    fig, ax = mpf.plot(ohlc, type='candle', xlabel=xlabel, ylabel=ylabel, figratio=(8,6), returnfig=True, **kwargs)
    ax[0].yaxis.set_label_position('left')
    ax[0].yaxis.tick_left()
    for i in ['top', 'bottom', 'left', 'right']:
        ax[0].spines[i].set_color('black')
    prettify(rotate=True)

def plot_candle_original( ohlc,
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
    plt.plot(x, y, **kwargs)
    if horizontal:
        for value in horizontal:
            plt.axhline(y=value, color='lightgrey', linestyle='dashed', zorder=0)
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
    if legend:
        plt.legend()
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

def save( name,
          show = False ):
    plt.savefig(f"outputs/{name}.png",bbox_inches='tight')
    if show: plt.show()
    else: plt.close()
