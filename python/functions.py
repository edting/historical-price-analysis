import numpy as np

# Number of consecutive days that the unit price increased or decreased
def countConsecutiveMovement(price):
    num_consec_incr = []
    num_consec_decr = []
    is_increasing = True #will flip to False when counting consecutive decreasing days
    count = 0
    for i in range(1,len(price)):
        # if counting consecutive decreases and find an increase in price (or vice versa),
        # append the count to the appropriate list, reset it, and start counting for the new case
        if price[i] > price[i-1]:
            if count > 0 and not is_increasing:
                num_consec_decr.append(count)
                count = 0
            is_increasing = True
            count += 1
        elif price[i] < price[i-1]:
            if count > 0 and is_increasing:
                num_consec_incr.append(count)
                count = 0
            is_increasing = False
            count += 1
        elif price[i] == price[i-1] and count > 0:
            # in case two consecutive days close at the same value, treat as either
            # increasing or decreasing depending on the trend that is currently being tracked
            # i.e assuming that count > 0, simply increment the count :)
            count += 1

        # on final iteration of the loop: append count to the appropriate list
        if i == len(price)-1 and count > 0:
            if is_increasing: num_consec_incr.append(count)
            else: num_consec_decr.append(count)

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
