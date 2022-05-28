# Get-Second-Chart
This script makes a candlestick data in very low time frames (seconds).

The candlestick data for cryptocurrencies are avalible in many platforms but the time frames are standard and very low timeframes are not avalible for free.

In this file the necessary means for making very low timeframe (1s) candlestick data (OHLCV) are provided. And also an example is provided in the file that generates candlestick data in 1s timeframe.

One very important thing about this script is that it uses binance's data and its integrated with it. So if you are using anotehr exchange's data, you have to change the column's names manully from code.

Also its good to note that because biannce's historical tardes are provided in milliseconds, you can lower the timeframe even more and get the candlestick data for millisecond candles (1ms 10ms 100ms etc.)
