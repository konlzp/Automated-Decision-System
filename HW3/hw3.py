'''
Created on Nov 8, 2015

@author: luozhipei
'''
import yahoo_finance
from datetime import datetime
from collections import defaultdict
from fileinput import close

global initialPrice

def getGains(stockHistory, duration, commission = 0):
    global initialPrice
    
    initialPrice = -1
    count = 0
    durationSum = 0
    prevDataPointer = 0
    bought = 0
    boughtPrice = 0
    gain = 0
    
    for dayData in stockHistory:
        if count < duration:
            count += 1
            durationSum += float(dayData['Adj_Close'])
        else:
            durationSum -= float(stockHistory[prevDataPointer]['Adj_Close'])
            durationSum += float(dayData['Adj_Close'])
            movAvg = durationSum / duration
            if not bought:
                if float(dayData['Adj_Close']) > movAvg:
                    bought = 1
                    gain -= float(dayData['Adj_Close']) * commission / 10000
                    boughtPrice = float(dayData['Adj_Close'])
                    if initialPrice == -1:
                        initialPrice = movAvg
            else:
                if float(dayData['Adj_Close']) < movAvg:
                    bought = 0
                    gain -= float(dayData['Adj_Close']) * commission / 10000
                    gain += float(dayData['Adj_Close']) - boughtPrice
            prevDataPointer += 1
    return gain / float(stockHistory[0]['Adj_Close'])

def backtest(ticker, start, end, duration = 50):
    global initialPrice
    try:
        startDate = datetime.strptime(start, '%Y-%m-%d')
        endDate = datetime.strptime(end, '%Y-%m-%d')
    except:
        print('wrong date format! Expect: %Y-%m-%d')
        return 
    

    stock = yahoo_finance.Share(ticker)
    stockHistory = stock.get_historical(start, end)
    stockHistory = stockHistory[::-1]

    if len(stockHistory) < duration:
        print('duration larger than Duration')
        return

    return (getGains(stockHistory, duration))
    
def sectortest(startdates = ['2005-01-01'], enddates = ['2006-10-01'], durations = [100], file = 'test2'):
    keys = ['XLV', 'XLF', 'XLU', 'XLE', 'XLK', 'XLY', 'XLP', 'XLB', 'XLI']
    sectorDict = defaultdict(list)
    
    bestRes = float('-inf')
    worstRes = float('inf')
    periodRes = [0 for i in range(0, len(startdates))]
    durationRes = [0 for i in range(0, len(durations))]
    
    for key in keys:
        periodDict = defaultdict(list)
        for periodCount in range(0, len(startdates)):
            durationDict = defaultdict(list)
            for durationCount in range(0, len(durations)):
                duration = durations[durationCount]
                result = backtest(key, startdates[periodCount], enddates[periodCount], duration)
                durationDict[duration] = result
                periodRes[periodCount] += result
                durationRes[durationCount] += result
                if result < worstRes:
                    worstRes = result
                    worstScene = [key, startdates[periodCount], enddates[periodCount], duration]
                if result > bestRes:
                    bestRes = result
                    bestScene = [key, startdates[periodCount], enddates[periodCount], duration]
            periodDict[periodCount] = durationDict
        sectorDict[key] = periodDict
    
    bestPeriod = max(periodRes)
    bestPIndex = periodRes.index(bestPeriod)
    bestDuration = max(durationRes)
    bestDIndex = durationRes.index(bestDuration)
    
    bestRes = bestRes
    worstRes = worstRes
    
    fd = open(file, 'wb')
    fd.write('best ' + bestScene[0] + ' ' + bestScene[1] + ' ' + bestScene[2] + ' ' + str(bestScene[3]) + ' ' + str(bestRes) + '\n')
    fd.write('worst '  + worstScene[0] + ' ' + worstScene[1] + ' ' + worstScene[2] + ' ' + str(worstScene[3]) + ' ' + str(worstRes) + '\n')
    fd.write('avg-period ' + startdates[bestPIndex] + ' ' + enddates[bestPIndex] + ' ' + str(bestPeriod / (len(durations) * 9)) + '\n')
    fd.write('avg-duration ' + str(durations[bestDIndex]) + ' ' +  str(bestDuration / (len(startdates) * 9)) + '\n')
    close()
    return sectorDict

def realbacktest(ticker = 'AAPL', start = '2014-01-01', end = '2015-10-23', duration = 20, commission = 2, file = 'test3'):
    global initialPrice

    try:
        startDate = datetime.strptime(start, '%Y-%m-%d')
        endDate = datetime.strptime(end, '%Y-%m-%d')
    except:
        print('wrong date format! Expect: %Y-%m-%d')
        return 
    
    if (endDate - startDate).days < duration:
        print('duration larger than Duration')
        return
    
    stock = yahoo_finance.Share(ticker)
    stockHistory = stock.get_historical(start, end)
    stockHistory = stockHistory[::-1]
    realGain = (getGains(stockHistory, duration, commission))
    
    fd = open(file, 'wb')
    fd.write(str(realGain) + ' net return, moving average\n')
    fd.write(str((float(stockHistory[-1]['Adj_Close']) - float(stockHistory[0]['Adj_Close'])) / float(stockHistory[0]['Adj_Close'])) + ' buy and hold return\n')
    close()

#sectortest()
#realbacktest()
#print(backtest('AAPL', '2014-01-01', '2015-10-23', 20))


