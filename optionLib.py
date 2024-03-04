import datetime as dt
from yahoo_fin import stock_info as si

def getExpiration():
    #prompt for appropriate expiration
    whichFri = input("Please input 'this' or 'next' or '+1' Friday: ")
 
    #baseline today's date
    today = dt.date.today()
    print("Today: ", dt.date.strftime(today, "%m/%d/%Y"))
    friday = today + dt.timedelta((4-today.weekday()) % 7)
    
    #if this Friday convert the nearest Friday to string
    if (whichFri == "this"):
        friStr = dt.date.strftime(friday, "%m/%d/%Y")
    #if +1 friday increment by 2 weeks and convert to string
    elif (whichFri == "+1"):
        friday = friday + dt.timedelta(14)
        friStr = dt.date.strftime(friday, "%m/%d/%Y")
    #else if next friday increment by 1 week and convert to string
    else:
        friday = friday + dt.timedelta(7)
        friStr = dt.date.strftime(friday, "%m/%d/%Y")

    return friStr

def getTickers():
    #prompt for appropriate Ticker set(
    whichTicker = input("Please choose 'sp' (for S&P) or 'd+' (for the DOW+): ")

    #if S&P
    if (whichTicker=="sp"):
        tickers = si.tickers_sp500()
    else:
        # get list of DOW tickers
        tickers = si.tickers_dow()

        #define extended or "+" list
        additional = ["BRK-B", "GOOGL", "AMZN", "NVDA", "TSLA", "LUV", "AAL", "UAL", "SPY", "DIA"]

        #add extended list to dow tickers
        tickers.extend(additional)

    return tickers

def getTarget():
    #prompt for appropriate Ticker set(
    whichTarget = input("Please choose 'L' (for last) or 'BA' (for bid-ask): ")

    # Validate that the input is either "L" or "BA"
    if whichTarget == "L" or whichTarget == "BA":    
        return whichTarget
    else: 
        print("Invalid input using 'BA' for bid-ask")
        return "BA"

#def printPutsArray(array):
#    for 
#    print("Ticker:", ticker, "(", name, ") Price:", round(current_price, 2), "Strike:",
#             strike, "Target Offer:", tPrice, "Yield:", tYield, "%")

