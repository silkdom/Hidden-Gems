
import requests
import pandas as pd
import json
import time as tt
import numpy as np



df_price = pd.read_csv("price_day2.csv")
df_price['time_h']=df_price['time']//(86400000/24)

final_price = pd.DataFrame(columns = ['coin','time','coin_price','symbol','time_h'])
    

p4 = list(df_price.symbol.unique())
for coin in p4:
    final_price = pd.concat([final_price,df_price.loc[df_price.symbol == coin].iloc[[-1]]])
        
    
p1 = list(final_price.symbol.unique())
p2 = list(df_price.symbol.unique())
p3 = list(np.setdiff1d(p2,p1))
for coin in p3:
    df_price = df_price[df_price.symbol != coin]
        


df_price.to_csv('df_price.csv',index=False)
final_price.to_csv('final_price.csv',index=False)