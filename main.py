from datetime import datetime, time
from pickle import TRUE
import string
import pandas as pd
import os
# This scipt gets file for historical tardes and returns
# an excel file containing candle sticks in the sprcified
# timeframe   

def timeFrames(TF:string) -> float:
    """
    This function receives a timeframe as a string and returns it as an integer (in milliseconds)

    Arguments
    ---------
        TF: string: The timeframe in string (e.g. 1m, 5m, 1d)

    Returns
    -------
        An integer representing the milliseconds timeframe consistes
    
    ** Remember that TF has to be always devisable by 1 day **
    """

    if(TF == "1s"):
        return 1000
    elif(TF == "10s"):
        return 1000 * 10 
    elif(TF == "30s"):
        return 1000 * 30 
    elif(TF == "1m"):
        return 1000 * 60 
    elif(TF == "5m"):
        return 1000 * 60 * 5
    elif(TF == "15m"):
        return 1000 * 60 * 15
    elif(TF == "30m"):
        return 1000 * 60 * 30
    elif(TF == "1h"):
        return 1000 * 60 * 60
    elif(TF == "4h"):
        return 1000 * 60 * 60 * 4
    elif(TF == "12h"):
        return 1000 * 60 * 60 * 12
    elif(TF == "1d"):
        return 1000 * 60 * 60 * 24

def get_day_start(unixTime:float) -> float:
    """
    Gets the start of the day's unix timestamp for a given day's unix time stamp. 
    
    Arguments
    ---------
        unixTime: float: the unix timestamp of a memont in the day (Milliseconds).

    Returns
    -------
        A float timestamp in milliseconds.

    """
    dt = datetime.fromtimestamp(unixTime/1000)
    dt = dt.replace(hour=0,second=0,minute=0,microsecond=0)
    
    return dt.timestamp()*1000

def get_latest_point(Path):
    """
    Generates a list of all the avalible (downloaded) tardes that are in files. Note
    that this fucntion only gets the first and last tarde that are in a file and not
    all the trades. this helps us know what trades are avalible for us and a certain 
    tradeId is in which file, so we can openning each file and searching through all
    the trades in it.

    Note that the files inside the folder has to be in the following format:
    f"/HistoricalTrades_{symbol}_{startId}____{endId}.xlsx"

    Arguments
    --------
        Path: string: The path to search for the downloaded trades (Files).
    
    Returns
    -------
        A list of the beginning and end tradeId in each file
    """
    ids = []
    for files  in os.listdir(Path):
        ls = files.replace(".xlsx","").split("_")
        # print(ls[2] + " => " + str(ls[6]))
        ids = pd.concat([ids, int(ls[2])]) 
        ids = pd.concat([ids, int(ls[6])])
    
    
    if(len(os.listdir(Path)) != 0):
        return max(ids)
    else:
        return -1

def ohlcv_generator(df:pd.DataFrame):
    """
    Gets a dataframe containing the transactions in a timestamp and turns all the
    transactions happened in this timestamp, to a japaneese candlestick. 
    
    Arguments
    ---------
        A dataframe of transactions happened in a timeframe. The columns are as follows:
        columns = ["id","time","price","qty","isBuyerMaker","isBestMatch"]. The last two
        columns are not really important and can be neglected.

    Returns
    -------
        A dataframe with one row. the columns are: ["time", "open", "high", "low", "close", "volume"] 
        "time" is the open time of the candle and qty is the quote asset volume
    """
    candle = pd.DataFrame(columns = ["time", "open", "high", "low", "close", "volume"])
    
    tempdf = pd.DataFrame([[
            datetime.fromtimestamp(df["time"].iloc[0]/1000), 
            df["price"].iloc[-1],
            df["price"].max(),
            df["price"].min(),
            df["price"].iloc[0],
            df["qty"].sum()
            ]], columns =  ["time", "open", "high", "low", "close", "volume"])

    candle = pd.concat([candle, tempdf])

    return candle

def save_dataframe(df:pd.DataFrame, name:string, DATAPATH:string):
    """
    Writes the dataframe to an excel file. 

    Arguments
    ---------
        df: pd.Dataframe(): The dataframe to write.
        name: string: The name of the xlsx file (The name string should have an xlsx extension)
        DATAPATH: string: The path to save the file (The DATAPATH string should have an xlsx extension)

    Returns
    -------
        None
    """

    #Make a historical tades directory
    exists = os.path.exists(DATAPATH)
    if not exists:
        os.makedirs(DATAPATH)

    with pd.ExcelWriter(name) as writer:
        df.to_excel(writer, index = False)


DATAPATH = "../../Data/HistoricalTrades/"
SAVEPATH = "../../DATA/GeneratedCandles/"
SYMBOL = "BTCUSDT"
TF = timeFrames("1s") # In milliseconds

for file  in os.listdir(DATAPATH):
    print(file)
    candles = pd.DataFrame(columns = ["time", "open", "high", "low", "close", "volume"])
    print(DATAPATH + file)
    trades = pd.read_pickle(DATAPATH + file)

    lastTX = trades.iloc[-1]["id"]
    lastTX_time = trades.iloc[-1]["time"]

    startDay = get_day_start(lastTX_time)
    Candle_time = startDay + (lastTX_time - startDay)//TF*TF

    # Getting the first candle (Probably not closed)
    df = ohlcv_generator(trades[(Candle_time<=trades["time"]) & (trades["time"]<=lastTX_time)])
    candles = pd.concat([candles, df], ignore_index= True)

    # getting the timestamp for oldest traded in files to know where we
    # are gonna stop
    endOfDataSetTime = trades.iloc[0]["time"]
    
    print("Starting new batch...")

    while True:
        tmp = Candle_time
        Candle_time = Candle_time - TF

        tmpDf = trades[(Candle_time<=trades["time"]) & (trades["time"]<tmp)]
        if(0 < tmpDf.shape[0]):
            df = ohlcv_generator(trades[(Candle_time<=trades["time"]) & (trades["time"]<tmp)])
        else:
            df = pd.DataFrame(
                [[datetime.fromtimestamp(Candle_time/1000) ,
                 candles["close"].iloc[-1],
                 candles["close"].iloc[-1],
                 candles["close"].iloc[-1],
                 candles["close"].iloc[-1],
                 0
                 ]], 
                columns = ["time", "open", "high", "low", "close", "volume"]
                )
        candles = pd.concat([candles, df], ignore_index = True)

        if( Candle_time-TF < endOfDataSetTime ):
            
            save_dataframe(candles, SAVEPATH + f"/GeneratedCandles_{SYMBOL}_{TF}_{trades.iloc[-1,1]}____{trades.iloc[0,1]}.xlsx", SAVEPATH )
            print("Saved to: " + f"/GeneratedCandles_{SYMBOL}_{TF}_{trades.iloc[-1,1]}____{trades.iloc[0,1]}.xlsx")
            break
    













# print(trades)