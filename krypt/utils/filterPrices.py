

def filterPrices(ethereumprices) :

    prices = []
    time =[]

    for i in ethereumprices :
        prices.append(i[1])
        time.append(i[0])

    prices = prices[::-1]
    time = time[::-1]
    return {
        'prices' : prices ,
        'time' : time ,
    }
