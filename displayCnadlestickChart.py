import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

"""
This file displays the candlestick data genereated by 
the "main.py" script in this folder. 
Note that the files ahs to be in the following format :
f"/GeneratedCandles_{SYMBOL}_{TF}_{startTime}____{endTime}.xlsx"
start and end time are in millisecond unix timestamps
"""
READPATH = "../../Data/GeneratedCandles/"
SYMBOL = "BTCUSDT"

backwardOffest = 0
referenceDate = 1561771800
forwardOffset =50

df = pd.read_excel(READPATH + "GeneratedCandles_BTCUSDT_1000_1650741363017____1650737820020.xlsx")

fig = go.Figure(data=[go.Candlestick(x=df['time'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

fig.show()