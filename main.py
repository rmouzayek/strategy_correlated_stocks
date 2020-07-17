import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn
import time


class Data: 
    def __init__(self, file_1, file_2, threshold=4):
        df_1 = pd.read_csv(file_1) 
        df_2 = pd.read_csv(file_2)
        df_1['jump'] = df_1['price'].diff()
        df_1['timestamp'] = pd.to_datetime(df_1.timestamp)
        df_2['timestamp'] = pd.to_datetime(df_2.timestamp)
        
        self.stock_1 = df_1
        self.stock_2 = df_2
        self.filtered_stock_1 = df_1[abs(df_1['jump']) > threshold]

class Order:
    def __init__(self, last_price, new_price):
        self.last_price = last_price
        self.new_price = new_price
        
    def buy_sell(self):
        return self.new_price - self.last_price 
    
    def sell_buy(self):
        return self.last_price - self.new_price
    
    def execute(self, value):
        if value > 0: 
            return self.buy_sell()
        else: 
            return self.sell_buy()
    
def extract_prices_2(time, df_2): 
    last = df_2.loc[(df_2['timestamp'] < time)].iloc[[-1]] # because we assume that at any given time T, 
    #we can buy or sell the stock at the last price that we had before T
    last_price = last['price'].values[0]   
    new_price = df_2.iloc[last.index[0] + 1]['price']
    return  Order(last_price, new_price)


def PnL(filtered_df_1, df_2, execution_lapse=40):
    pnl = 0 
    for index, row in filtered_df_1.iterrows():
        current_time = row['timestamp']
        execution_time = current_time + pd.Timedelta(milliseconds=execution_lapse)
        current_order = extract_prices_2(execution_time, df_2)
        pnl += current_order.execute(row['jump'])
    return pnl



if __name__ == '__main__': 
    Tables = Data('4708263_FGA0ZWBR.csv', '4708263_QB3Z8L4T.csv')
    print('The PnL of the initial algorithm is {}'.format(PnL(Tables.filtered_stock_1, Tables.stock_2)))
    
    ### Variation: 
    ### What is the largest value of M for which the algorithm is profitable?
    X = [m for m in range(40, 150, 20)]
    Y = [PnL(Tables.filtered_stock_1, Tables.stock_2, m) for m in range(40, 150, 20)]
    plt.xlabel('execution time')
    plt.ylabel('PnL')
    plt.title('PnL of the strategy with respect to the execution time')
    plt.plot(X, Y)
    
    
    X = [m for m in range(85, 95, 1)]
    Y = [PnL(Tables.filtered_stock_1, Tables.stock_2, m) for m in range(85, 95, 1)]
    print(dict(zip(X, Y)))
    
    print('According to the plot, it is between 85 and 95.\n The last M is 90 ms.')