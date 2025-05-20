# Number of consecutive days that the unit price increased or decreased
def calculateConsecutiveMovement(price):
    numberConsecutiveIncreasing = []
    numberConsecutiveDecreasing = []
    countIncreasing = True #will flip to False when counting consecutive decreasing days
    count = 0
    for i in range(1,len(price)):
        if price[i] > price[i-1]:
            # if we were counting consecutive decreasing days, append to the list and reset the count
            if count > 0 and not countIncreasing:
                numberConsecutiveDecreasing.append(count)
                count = 0

            # start counting consecutive increasing days
            countIncreasing = True
            count += 1
        elif price[i] < price[i-1]:
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
        if i == len(price)-1 and count > 0:
            if countIncreasing: numberConsecutiveIncreasing.append(count)
            else: numberConsecutiveDecreasing.append(count)

    return numberConsecutiveIncreasing, numberConsecutiveDecreasing
