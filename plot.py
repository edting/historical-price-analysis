import pandas as pd
import matplotlib.pyplot as plt

# read csv
vgs = pd.read_csv("vgs.csv")
vgs = vgs.iloc[::-1] #csv is in reverse chronological order; this line inverts it
vgs['Date'] = pd.to_datetime(vgs['Date'], format='%d/%m/%Y') #convert dates from str to datetime object
#print(vgs)

# plot utils
def plot_line(x, y, xlabel="x", ylabel="y", name=""):
    fig = plt.plot(x, y)
    prettify(fig, xlabel, ylabel, rotate=True)
    plt.show()
    if name: save(fig, name)

def plot_hist(values, range=(0,10), nbins=10, xlabel="Values", ylabel="Frequency", name=""):
    fig = plt.hist(values, nbins)
    prettify(fig, xlabel, ylabel)
    plt.show()
    if name: save(fig, name)

def prettify(fig, xlabel="x", ylabel="y", rotate=False):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if rotate: plt.xticks(rotation=45, fontsize='small')
    plt.tight_layout()

def save(fig, name):
    plt.savefig(f"{name}.pdf")    
    
# PLOT
date = vgs['Date'].to_numpy()
close = vgs['Price'].to_numpy()
fluctuation = vgs['High'].to_numpy() - vgs['Low'].to_numpy()

plot_line(date, close, xlabel="Date", ylabel="Close price [$]", name="price")
plot_line(date, fluctuation, xlabel="Date", ylabel="Daily price fluctuation [$]", name="day_range")

# calculate and plot the number of consecutive days that the unit price increased
numberConsecutiveIncreasing = []
count = 0
for i in range(1,len(close)):
    if close[i] > close[i-1]:
        count += 1
    else:
        numberConsecutiveIncreasing.append(count)
        count = 0

print(numberConsecutiveIncreasing)
print(close)
xmin = min(numberConsecutiveIncreasing)
xmax = max(numberConsecutiveIncreasing)
nbins = xmax - xmin
plot_hist(numberConsecutiveIncreasing, range=(xmin,xmax), nbins=nbins, xlabel="Number of consecutive price increases", name="consecutive_increase")
