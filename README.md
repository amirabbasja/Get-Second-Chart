This script makes a candlestick data in very low time frames (seconds, milliseconds).


**Abstract**

The candlestick data for cryptocurrencies are avalible in many platforms but the time frames are standard and very low timeframes are not avalible for free.

In this file the necessary means for making very low timeframe (1s) candlestick data (OHLCV) are provided. And also an example is provided in the file that generates candlestick data in 1s timeframe.



**Logic**

This conde gets the historical trades done in a time period and aggregates the trades in this range in desired intervals and generates japaneese candlestick data for this range and exports it as  a file.

One very important thing about this script is that it uses binance's data and its integrated with it. So if you are using anotehr exchange's data, you have to change the column's names manully from code.

Also its good to note that because biannce's historical tardes are provided in milliseconds, you can lower the timeframe even more and get the candlestick data for millisecond candles (1ms 10ms 100ms etc.)


**How to work with this script**

Because i needed to change a large amount of trades to LFT(Low timeframe) candlesticks, The code is designed to get all the files in a folder and generate the candlestick data for each file and save the candlestick data to another path. But if you want to read a single file, you can only put one file in the said folder.

Another thing to note is for to increase performance of the script, we have saved the transactions as a dataframe in the format pf a pickle file. and we use pandas's read_pickle method to load the trades.

 if you want to change the method of loading the input data, change the following line to the method you desire:
 

    trades = pd.read_pickle(DATAPATH + file)

 Also it's necessary to note that there are three constants you need to assign before starting the program:
  

 - DATAPATH: The path you have saved your historical trades data
 - SAVEPATH: The path you want to save your candlestick data to
 - TF: the timeframe you want your candles to have (e.g. 1s, 10s and 30s). If you other timeframes, please change "timeFrames" method to your desire. Also if you want millisecond candles you have to add this manually to this method.

IMPORTANT: Your historical trades has to be in the following format (The file's format depends on your method of reading the files. xlsx is for reading excel files but pickle files does'nt have any general extensions):

    f"/HistoricalTrades_{symbol}_{startId}____{endId}.xlsx"


