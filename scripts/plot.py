import pandas as pd
import matplotlib.pyplot as plt

# Read csv
vgs = pd.read_csv("../data/vgs.csv")
vgs = vgs.iloc[::-1] #csv is in reverse chronological order; this line inverts it
vgs['Date'] = pd.to_datetime(vgs['Date'], format='%d/%m/%Y') #convert dates from str to datetime object
vgs['Vol.'] = vgs['Vol.'].str.replace('K','') #this is formatted like 100.00K in the csv
vgs['Change %'] = vgs['Change %'].str.replace('%','')
vgs = vgs.astype({'Vol.':float, 'Change %':float}) #specify value types

# Extract information from the dataframe
date = vgs['Date'].to_numpy()
open_price = vgs['Open'].to_numpy()
close_price = vgs['Price'].to_numpy()
max_price = vgs['High'].to_numpy()
min_price = vgs['Low'].to_numpy()
volume = vgs['Vol.'].to_numpy()*1000
change = vgs['Change %'].to_numpy()
fluctuation = max_price - min_price
fluctuation_end = close_price - open_price
fluctuation_ratio = abs(fluctuation_end) / fluctuation

#--------------------
# Plotting functions
#--------------------
def plot_line(x, y, xlabel="x", ylabel="y", horizontal=[]):
    if horizontal:
        for value in horizontal:
            plt.axhline(y=value, color='lightgrey', linestyle='dashed')
    plt.plot(x, y)
    prettify(xlabel, ylabel, rotate=True)

def plot_hist(values, axisrange=None, nbins=50, color="royalblue", alpha=0.5, xlabel="Values", ylabel="Frequency", legend=""):
    plt.hist(values, range=axisrange, bins=nbins, color=color, alpha=alpha, label=legend)
    prettify(xlabel, ylabel)

def prettify(xlabel="", ylabel="", rotate=False):
    if xlabel: plt.xlabel(xlabel)
    if ylabel: plt.ylabel(ylabel)
    if rotate: plt.xticks(rotation=45, fontsize='small')
    plt.tight_layout()

def save(name, show=False):
    plt.savefig(f"../outputs/{name}.pdf")
    if show: plt.show()
    else: plt.close()

#------
# PLOT
#------

# to use as legend label in some histograms
daterange = f"{str(date[0])[:10]} to {str(date[-1])[:10]}"

# Closing price (time series)
plot_line(date, close_price, xlabel="Date", ylabel="Close price [$]")
save("price", show=False)

# Daily maximum fluctuation (time series)
plot_line(date, fluctuation, xlabel="Date", ylabel="Daily maximum price fluctuation [$]", horizontal=[0.5,1])
save("day_range", show=False)

# Daily maximum fluctuation (histogram)
plot_hist(fluctuation, xlabel="Daily maximum price fluctuation [$]", legend=daterange)
plt.legend()
save("day_range_binned", show=False)

# Daily open minus close (time series)
plot_line(date, fluctuation_end, xlabel="Date", ylabel="Daily open-close difference [$]", horizontal=[0])
save("open_close_difference", show=False)

# Daily open minus close (histogram)
plot_hist(fluctuation_end, xlabel="Daily open-close difference [$]", legend=daterange)
plt.legend()
save("open_close_difference_binned", show=False)

# Ratio of daily end-to-end fluctuation to the maximum fluctuation
plot_hist(fluctuation_ratio, nbins=10, xlabel="|open - close| / maximum fluctuation", legend=daterange)
plt.legend()
save("fluctuation_ratio", show=False)

# Trading volume
plot_hist(volume, xlabel="Trading volume", legend=daterange)
plt.legend()
save("volume", show=False)

# Daily relative change
plot_line(date, change, xlabel="Date", ylabel="Relative change [%]", horizontal=[0])
save("change", show=False)

# Number of consecutive days that the unit price increased or decreased
numberConsecutiveIncreasing = []
numberConsecutiveDecreasing = []
countIncreasing = True #will flip to False when counting consecutive decreasing days
count = 0
for i in range(1,len(close_price)):
    if close_price[i] > close_price[i-1]:
        # if we were counting consecutive decreasing days, append to the list and reset the count
        if count > 0 and not countIncreasing:
            numberConsecutiveDecreasing.append(count)
            count = 0

        # start counting consecutive increasing days
        countIncreasing = True
        count += 1
    elif close_price[i] < close_price[i-1]:
        if count > 0 and countIncreasing:
            numberConsecutiveIncreasing.append(count)
            count = 0
        countIncreasing = False
        count += 1
    else:
        # in case two consecutive days close at the same value
        if count > 0:
            if countIncreasing:
                numberConsecutiveIncreasing.append(count)
            else:
                numberConsecutiveDecreasing.append(count)

        # reset count
        count = 0

    # on final iteration: append count to the corresponding list
    if i == len(close_price)-1 and count > 0:
        if countIncreasing: numberConsecutiveIncreasing.append(count)
        else: numberConsecutiveDecreasing.append(count)
    

xmin = min( min(numberConsecutiveIncreasing), min(numberConsecutiveDecreasing) )
xmax = max( max(numberConsecutiveIncreasing), max(numberConsecutiveDecreasing) )
nbins = xmax - xmin
plot_hist(numberConsecutiveIncreasing, axisrange=(xmin,xmax), nbins=nbins, xlabel="Number of consecutive days", legend="Increasing")
plot_hist(numberConsecutiveDecreasing, axisrange=(xmin,xmax), nbins=nbins, color="sienna", xlabel="", legend="Decreasing")
plt.legend()
save("consecutive_days", show=False)

# For the days where open price > close price: plot the change % for the following day
following_negative_change = [ val for i,val in enumerate(change[1:]) if open_price[i-1] > close_price[i-1] ]
following_positive_change = [ val for i,val in enumerate(change[1:]) if open_price[i-1] < close_price[i-1] ]
plot_hist(following_positive_change, xlabel="Change [%]", legend="Next day after positive growth (close > open)")
plot_hist(following_negative_change, color="sienna", xlabel="", legend="Next day after negative growth (open > close)")
plt.legend()
save("following_day_change", show=True)
