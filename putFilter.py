import yahoo_fin.options as ops
from yahoo_fin import stock_info as si
from tqdm import tqdm
import time
import os
from optionLib import *
from operator import itemgetter

putsArray = []

friStr = getExpiration()
#friStr = "04/06/2023" for Easter

print(f"Expiration = {friStr}")

tickers = getTickers()

lastortarget = getTarget()

if (len(tickers) > 50):
    hold=8
    print("Warning: the ticker set is large and will need to run longer to avoid blocking from Yahoo")
else:
    hold=0

# mvp ticker = "AAPL"  # replace with the ticker symbol of the stock you're interested in
# pull data for each Tickers (DOW, Extended) stock

#writes the ticker information to a "load" file in case the server shutsdown
#mostly needed for s&p
with open('loadTickers.txt', 'w') as f:
    #for ticker in tickers, and use tqdm to display progress
    for ticker in tqdm(tickers, desc="Loading tickers", unit="tickers", dynamic_ncols=False):
        #sleep required for S&P
        time.sleep(hold)
        try: 
            current_price = si.get_live_price(ticker)    
            # calculates the strike price that is 5% out of the money
            strike_price = round(current_price * 0.95, 2)

            # 'try' to get all put options for the given expiration date
            try:
                put_options = ops.get_puts(ticker, friStr)
            except ValueError:
                put_options = None

            # if it did get options:
            if put_options is not None:
                # sorts the put options by their strike price
                put_options = put_options.sort_values(by=["Strike"])

                # finds the put option with the strike price closest to `strike_price`
                closest_strike_put = put_options.iloc[(
                    put_options["Strike"] - strike_price).abs().argsort()[:1]]

      
                # gets the bid, ask of the option
                strike = closest_strike_put.loc[closest_strike_put.index[0], "Strike"]
                name = closest_strike_put.loc[closest_strike_put.index[0],
                      "Contract Name"]
                last = closest_strike_put.loc[closest_strike_put.index[0], "Last Price"]
                ask = closest_strike_put.loc[closest_strike_put.index[0], "Ask"]
                # gets the implied volatility, which can be used to calculate the yield
                bid = closest_strike_put.loc[closest_strike_put.index[0], "Bid"]

                #calculate yield based lastORtarget choice
                if lastortarget == "L":
                    tPrice = round(float(last), 2)
                elif lastortarget == "BA":
                    tPrice = round((float(ask)+float(bid))/2, 2)
                tYield = round(5200*((tPrice/strike)), 2)

                #load to array for sorting 
                putsArray.append([ticker, name, round(current_price, 2), strike, tPrice, tYield])

                #write to loadfile as back-up
                f.write(f"Ticker: {ticker} ({name}) Price: {round(current_price, 2)} Strike: {strike} Target Offer: {tPrice} Yield: {tYield} %\n")
            else:
                # handle the case where no options available
                print(f"No put options found for {ticker} on {friStr} removing from puts Array")
    
        except AssertionError as e:
            print(f"Error getting live price for {ticker}: {e}")
            continue # move on to the next ticker

#sort the putsArray
spArray = sorted(putsArray, key=itemgetter(5), reverse=True)

#write sorted putsArray to file
with open('putsYield.txt', 'w') as f:
    for i, row in enumerate(spArray):
        f.write(f"Ticker: {row[0]} ({row[1]}) Price: {row[2]} Strike: {row[3]} Target Offer: {row[4]} Yield: {row[5]}%\n")

#remove the temp 'loadTickers.txt'
os.remove('loadTickers.txt')