import numpy as np

def consecutive_movement(price):
    """
    Study the lengths and strengths of consecutive movements in market price.

    Implementation:
    Split price data into consecutively increasing or decreasing segments.
    For each of these segments, determine the number of periods in the segment,
    and also fit a straight line and extract the slope of the segment.

    Returns a packed tuple: 1. list of lengths of increasing segments
                            2. list of lengths of decreasing segments
                            3. list of slopes of increasing segments
                            4. list of slopes of decreasing segments
    """
    num_consec_incr = []
    num_consec_decr = []
    slope_incr = []
    slope_decr = []

    num_incr = num_decr = 0
    price = prune_leading_bears(price)
    for i in range(1,len(price)):
        if price[i] > price[i-1] and num_decr > 0:
            num_consec_incr.append(num_incr)
            num_consec_decr.append(num_decr)

            increasing_period = list(range(num_incr+1))
            increasing_segment = price[i-1-num_decr-num_incr:i-num_decr]
            increasing_slope = np.polyfit(increasing_period, increasing_segment, 1)[0]
            slope_incr.append(increasing_slope)

            decreasing_period = list(range(num_decr+1))
            decreasing_segment = price[i-1-num_decr:i]
            decreasing_slope = np.polyfit(decreasing_period, decreasing_segment, 1)[0]
            slope_decr.append(decreasing_slope)

            num_incr = num_decr = 0

        num_incr, num_decr = increment_counts(num_incr, num_decr, price[i], price[i-1])

        # On final iteration, append counts to the corresponding list
        if i == len(price)-1:
            if num_incr > 0: num_consec_incr.append(num_incr)
            if num_decr > 0: num_consec_decr.append(num_decr)

    return num_consec_incr, num_consec_decr, slope_incr, slope_decr

def prune_leading_bears(price):
    """
    Trims the start of price data so that it begins with a period of increasing price.
    """
    n = 0
    for i in range(1,len(price)):
        if price[i] <= price[i-1]:
            n += 1
        else:
            break
    return price[n:]

def increment_counts(num_incr, num_decr, current, previous):
    """
    Increment counters for consecutive increasing / decreasing days.
    If two consecutive days close at the same price, treat as increasing
    or decreasing depending on the trend that is currently being tracked.
    """
    if current > previous:
        return num_incr+1, num_decr
    elif current < previous:
        return num_incr, num_decr+1
    elif current == previous:
        if num_decr > 0: return num_incr, num_decr+1
        elif num_incr > 0: return num_incr+1, num_decr
