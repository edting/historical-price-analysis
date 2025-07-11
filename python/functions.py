import numpy as np

# Counts the number of consecutive days that the unit price increased or decreased
# Returns two lists `num_consec_incr, num_consec_decr` containing the counts for each case
def countConsecutiveMovement(price):
    num_consec_incr = []
    num_consec_decr = []
    num_incr = num_decr = 0
    price = pruneLeadingBears(price)
    for i in range(1,len(price)):
        if price[i] > price[i-1] and num_decr > 0:
            num_consec_incr.append(num_incr)
            num_consec_decr.append(num_decr)
            num_incr = num_decr = 0

        # increment counters
        num_incr, num_decr = incrementCounts(num_incr, num_decr, price[i], price[i-1])

        # on final iteration: append the counts to their corresponding list
        if i == len(price)-1:
            if num_incr > 0: num_consec_incr.append(num_incr)
            if num_decr > 0: num_consec_decr.append(num_decr)
    return num_consec_incr, num_consec_decr

# Number of consecutive decreases that follow each increasing period ("momentum" of the flip)
def flipMomentum(price):
    momentum = []
    num_incr = num_decr = 0
    price = pruneLeadingBears(price)
    for i in range(1,len(price)):
        # if prices start to increase again after a period of decreases,
        # append the counts to the 2D array and restart the process
        if price[i] > price[i-1] and num_decr > 0:
            momentum.append([num_incr, num_decr])
            num_incr = num_decr = 0

        # increment counters
        num_incr, num_decr = incrementCounts(num_incr, num_decr, price[i], price[i-1])

    return momentum

# Slopes of successive increasing -> decreasing periods ("strength" of the flip)
def flipStrength(price):
    strength = []
    num_incr = num_decr = 0
    price = pruneLeadingBears(price)
    for i in range(1,len(price)):
        # if prices start to increase again after a period of decreases,
        # append the ratio of their slopes then restart the process
        if price[i] > price[i-1] and num_decr > 0:
            increasing_period = list(range(num_incr+1))
            increasing_price = price[i-1-num_decr-num_incr:i-num_decr]
            increasing_slope = np.polyfit(increasing_period, increasing_price, 1)[0]

            decreasing_period = list(range(num_decr+1))
            decreasing_price = price[i-1-num_decr:i]
            decreasing_slope = np.polyfit(decreasing_period, decreasing_price, 1)[0]

            strength.append([increasing_slope, decreasing_slope])
            num_incr = num_decr = 0

        # increment counters
        num_incr, num_decr = incrementCounts(num_incr, num_decr, price[i], price[i-1])
        
    return strength
    
# Trim the start of a list so that it begins with a period of increasing price
def pruneLeadingBears(price):
    n = 0
    for i in range(1,len(price)):
        if price[i] <= price[i-1]:
            n += 1
        else:
            break
    return price[n:]

# Increment counters for consecutive increasing / decreasing days
# If two consecutive days close at the same price, treat as increasing or decreasing
# depending on the trend that is currently being tracked
def incrementCounts(num_incr, num_decr, today, yesterday):
    if today > yesterday:
        return num_incr+1, num_decr
    elif today < yesterday:
        return num_incr, num_decr+1
    elif today == yesterday:
        if num_decr > 0: return num_incr, num_decr+1
        elif num_incr > 0: return num_incr+1, num_decr
