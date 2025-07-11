import numpy as np

# Analyse consecutive movement of the unit price
def consecutiveMovement(price):
    # Initialise lists to be returned
    num_consec_incr = [] # number of consecutive price increases
    num_consec_decr = [] # number of consecutive price decreases
    slope_incr = []      # linear gradient of the increasing period
    slope_decr = []      # linear gradient of the decreasing period

    # Loop over the prices and track consecutive periods
    num_incr = num_decr = 0
    price = pruneLeadingBears(price)
    for i in range(1,len(price)):
        # append quantities of interest to corresponding outputs
        if price[i] > price[i-1] and num_decr > 0:
            # number of consecutive increases and decreases
            num_consec_incr.append(num_incr)
            num_consec_decr.append(num_decr)

            # fit 1st order polynomials to extract linear gradient
            increasing_period = list(range(num_incr+1))
            increasing_price = price[i-1-num_decr-num_incr:i-num_decr]
            increasing_slope = np.polyfit(increasing_period, increasing_price, 1)[0]
            slope_incr.append(increasing_slope)
            
            decreasing_period = list(range(num_decr+1))
            decreasing_price = price[i-1-num_decr:i]
            decreasing_slope = np.polyfit(decreasing_period, decreasing_price, 1)[0]
            slope_decr.append(decreasing_slope)
            
            # reset counters
            num_incr = num_decr = 0

        # increment counters
        num_incr, num_decr = incrementCounts(num_incr, num_decr, price[i], price[i-1])

        # on final iteration: append the counts to their corresponding list
        if i == len(price)-1:
            if num_incr > 0: num_consec_incr.append(num_incr)
            if num_decr > 0: num_consec_decr.append(num_decr)

    return num_consec_incr, num_consec_decr, slope_incr, slope_decr
    
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
def incrementCounts(num_incr, num_decr, current, previous):
    if current > previous:
        return num_incr+1, num_decr
    elif current < previous:
        return num_incr, num_decr+1
    elif current == previous:
        if num_decr > 0: return num_incr, num_decr+1
        elif num_incr > 0: return num_incr+1, num_decr
