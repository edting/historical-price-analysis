# Count number of consecutive days that the unit price increased or decreased
def countConsecutiveMovement(price):
    numberConsecutiveIncreasing = []
    numberConsecutiveDecreasing = []
    countIncreasing = True #will flip to False when counting consecutive decreasing days
    count = 0
    for i in range(1,len(price)):
        # if counting consecutive decreases and find an increase in price (or vice versa),
        # append the count to the appropriate list, reset it, and start counting for the new case
        if price[i] > price[i-1]:
            if count > 0 and not countIncreasing:
                numberConsecutiveDecreasing.append(count)
                count = 0
            countIncreasing = True
            count += 1
        elif price[i] < price[i-1]:
            if count > 0 and countIncreasing:
                numberConsecutiveIncreasing.append(count)
                count = 0
            countIncreasing = False
            count += 1
        elif price[i] == price[i-1] and count > 0:
            # in case two consecutive days close at the same value, treat as either
            # increasing or decreasing depending on the trend that is currently being tracked
            # i.e assuming that count > 0, simply increment the count :)
            count += 1

        # on final iteration of the loop: append count to the appropriate list
        if i == len(price)-1 and count > 0:
            if countIncreasing: numberConsecutiveIncreasing.append(count)
            else: numberConsecutiveDecreasing.append(count)

    return numberConsecutiveIncreasing, numberConsecutiveDecreasing

# For each period of consecutive increases, count the number of consecutive decreases that follow
def flipStrength(price):
    flip = []
    num_incr = num_decr = 0
    skip = True
    for i in range(1,len(price)):
        # ignore consecutive decreasing days at the start
        if skip:
            if price[i] <= price[i-1]:
                continue
            else:
                skip = False #start the actual loop after we reach this point

        # if prices start to increase again after a period of decreases,
        # append the counts to the 2D array and restart the process
        if price[i] > price[i-1] and num_decr > 0:
            flip.append([num_incr, num_decr])
            num_incr = num_decr = 0

        # increment consecutive increasing / decreasing counts
        # in case two consecutive days close at the same value, treat as either
        # increasing or decreasing depending on the trend that is currently being tracked
        if price[i] > price[i-1]:
            num_incr += 1
        elif price[i] < price[i-1]:
            num_decr += 1
        elif price[i] == price[i-1]:
            if num_decr > 0: num_decr += 1
            elif num_incr > 0: num_incr += 1

    return flip
