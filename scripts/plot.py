import pandas as pd
import matplotlib.pyplot as plt

# read csv
vgs = pd.read_csv("../data/vgs.csv")
vgs = vgs.iloc[::-1] #csv is in reverse chronological order; this line inverts it
vgs['Date'] = pd.to_datetime(vgs['Date'], format='%d/%m/%Y') #convert dates from str to datetime object
#print(vgs)

# plot utils
def plot_line(x, y, xlabel="x", ylabel="y", name=""):
    fig = plt.plot(x, y)
    prettify(fig, xlabel, ylabel, rotate=True)
    if name: save(fig, name)
    plt.show()

def plot_hist(values, range=(0,10), nbins=10, xlabel="Values", ylabel="Frequency", name=""):
    fig = plt.hist(values, nbins)
    prettify(fig, xlabel, ylabel)
    if name: save(fig, name)
    plt.show()

def prettify(fig, xlabel="x", ylabel="y", rotate=False):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if rotate: plt.xticks(rotation=45, fontsize='small')
    plt.tight_layout()

def save(fig, name):
    plt.savefig(f"../outputs/{name}.pdf")    
    
# PLOT
date = vgs['Date'].to_numpy()
open_price = vgs['Open'].to_numpy()

close_price = vgs['Price'].to_numpy()
max_fluctuation = vgs['High'].to_numpy() - vgs['Low'].to_numpy()

plot_line(date, close_price, xlabel="Date", ylabel="Close price [$]", name="price")
plot_line(date, max_fluctuation, xlabel="Date", ylabel="Daily price fluctuation [$]", name="day_range")

# Number of consecutive days that the unit price increased
numberConsecutiveIncreasing = []
count = 0
for i in range(1,len(close_price)):
    if close_price[i] > close_price[i-1]:
        count += 1
    else:
        numberConsecutiveIncreasing.append(count)
        count = 0

xmin = min(numberConsecutiveIncreasing)
xmax = max(numberConsecutiveIncreasing)
nbins = xmax - xmin
plot_hist(numberConsecutiveIncreasing, range=(xmin,xmax), nbins=nbins, xlabel="Number of consecutive price increases", name="consecutive_increase")
