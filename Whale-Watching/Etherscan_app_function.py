import requests
import pandas as pd
import json
import time as tt
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st




st.title('Etherscan')



df_price = pd.read_csv("df_price.csv")
final_price = pd.read_csv("final_price.csv")


uniswap_addresses = pd.read_csv("uni.csv") 



@st.cache
def uniswap(address,df_price,final_price,uniswap_addresses):
    apikey = 'xxxxxxxxxxxxxxxxxxxxxxxx'
    response = requests.get('http://api.etherscan.io/api?module=account&action=tokentx&address='+address+'&startblock=0&endblock=999999999&sort=asc&apikey='+apikey)
    data = response.json()
    keys = [*data['result'][0]]
    df = pd.DataFrame(columns=keys, )
    
    blockNumber = []
    timeStamp = []
    hash_ = []
    nonce = []
    blockHash = []
    from_ = []
    contractAddress = []
    to = []
    value = []
    tokenName = []
    tokenSymbol = []
    tokenDecimal = []
    transactionIndex = []
    gas = []
    gasPrice = []
    gasUsed = []
    cumulativeGasUsed = []
    input_ = []
    confirmations = []
    for i in range(len(data['result'])):
        blockNumber.append(data['result'][i]['blockNumber'])
        timeStamp.append(data['result'][i]['timeStamp'])
        hash_.append(data['result'][i]['hash'])
        nonce.append(data['result'][i]['nonce'])
        blockHash.append(data['result'][i]['blockHash'])
        from_.append(data['result'][i]['from'])
        contractAddress.append(data['result'][i]['contractAddress'])
        to.append(data['result'][i]['to'])
        value.append(data['result'][i]['value'])
        tokenName.append(data['result'][i]['tokenName'])
        tokenSymbol.append(data['result'][i]['tokenSymbol'])
        tokenDecimal.append(data['result'][i]['tokenDecimal'])
        transactionIndex.append(data['result'][i]['transactionIndex'])
        gas.append(data['result'][i]['gas'])
        gasPrice.append(data['result'][i]['gasPrice'])
        gasUsed.append(data['result'][i]['gasUsed'])
        cumulativeGasUsed.append(data['result'][i]['cumulativeGasUsed'])
        input_.append(data['result'][i]['input'])
        confirmations.append(data['result'][i]['confirmations'])


    df = pd.DataFrame({'blockNumber': blockNumber,
    'timeStamp': timeStamp,
    'hash_':hash_,
    'nonce': nonce,
    'blockHash': blockHash,
    'from_': from_,
    'contractAddress': contractAddress,
    'to': to,
    'value': value,
    'tokenName': tokenName,
    'tokenSymbol': tokenSymbol,
    'tokenDecimal': tokenDecimal,
    'transactionIndex': transactionIndex,
    'gas': gas,
    'gasPrice': gasPrice,
    'gasUsed': gasUsed,
    'cumulativeGasUsed': cumulativeGasUsed,
    'input_': input_,
    'confirmations': confirmations})
    

    
    
    df = df.assign(buy=0)
    df = df.assign(sell=0)
    for i, j in df.iterrows():
        for k in uniswap_addresses['0']:
            if from_[i] == k:
                df.at[i,'buy'] = 1
            if to[i] == k:
                df.at[i,'sell'] = 1

    
    df = df.assign(time_h=0.0)
    df = df.assign(amount=0.0)
    for index, row in df.iterrows():
        df.at[index,'time_h'] = round(int(row.timeStamp)/(86400/24))
        df.at[index,'amount'] = float(row.value)/float((10**float(row.tokenDecimal)))
        df.at[index,'symbol'] = row.tokenSymbol.lower()
    
    
    df_trans = df.merge(df_price, on=['symbol','time_h'])
    
    df_trans['cost'] = df_trans['amount']*df_trans['coin_price']
    df_trans['buy_sell']=df_trans.sell+df_trans.buy
    df_aa = df_trans[(df_trans.buy_sell == 1)]
    df_bb = df_aa[['sell','symbol','buy','time_h','amount','coin_price','cost']]
    df_cc = df_bb
    portfolio = list(df_cc.symbol.unique())
    
    
    
    df_cc = df_cc.assign(test=0.0)
    df_cc = df_cc.assign(invent=0.0)
    df_cc = df_cc.assign(sold=0.0)
    df_cc = df_cc.assign(bought=0.0)
    for coin in portfolio:
        index_lag = df_cc.loc[df_cc['symbol'] == coin].head(1).index
        for index, row in df_cc.loc[df_cc['symbol'] == coin].iterrows():

            if row.buy == 1:
                df_cc.at[index,'invent'] = df_cc.invent[index_lag] + row.amount
                df_cc.at[index,'bought'] = row.amount
            if row.sell == 1:

                if float(df_cc.invent[index_lag]) > row.amount:

                    df_cc.at[index,'sold'] = row.amount
                    df_cc.at[index,'invent'] = df_cc.invent[index_lag] - row.amount
                elif float(df_cc.invent[index_lag]) > 0:

                    df_cc.at[index,'sold'] = df_cc.invent[index_lag]
                    df_cc.at[index,'invent'] = 0
            index_lag = index
  
    
    df_cc['inflow']=df_cc['coin_price']*df_cc['sold']
    df_cc['outflow']=df_cc['coin_price']*df_cc['bought']
    df_dd = df_cc

    df_dd = df_dd.assign(remaining=0.0)
    df_dd = df_dd.assign(salvage=0.0)
    for coin in portfolio:
        for index, row in df_dd.loc[df_dd['symbol'] == coin].iterrows():
            i = index

        df_dd.at[i,'salvage'] = df_dd['invent'][i]*float(final_price.loc[final_price['symbol']==coin].coin_price)
        df_dd.at[i,'remaining'] = df_dd['invent'][i]
    
    
    a = []
    b = []
    c = []
    d = []
    e = []
    f = []
    g = []
    h = []
    i = []
    j = []
    for coin in portfolio:
        df_temp = df_dd.loc[df_dd['symbol'] == coin].groupby(['symbol']).sum()
        a.append(coin)
        b.append(df_temp['buy'][0])
        c.append(df_temp['sell'][0])
        d.append(df_temp['bought'][0])
        e.append(df_temp['sold'][0])
        f.append(df_temp['outflow'][0])
        g.append(df_temp['inflow'][0])
        h.append(df_temp['remaining'][0])
        i.append(df_temp['salvage'][0])
        j.append(float(final_price.loc[final_price['symbol']==coin].coin_price))

    
    
    df_final = pd.DataFrame({'coin': a,
    'buy': b,
    'sell': c,
    'bought': d,
    'sold': e,
    'outflow': f,
    'inflow': g,
    'remaining': h,
    'salvage': i,
    'final_price': j})

    df_final['profit']=df_final['inflow']+df_final['salvage']-df_final['outflow']
    df_final['avg_buy']=df_final['outflow']/df_final['bought']
    df_final['avg_sell']=df_final['inflow']/df_final['sold']
    df_final['weighted_avg_sell']=(df_final['inflow']/df_final['sold'])*(df_final['sold']/(df_final['sold']+df_final['remaining']))+(df_final['salvage']/df_final['remaining'])*(df_final['remaining']/(df_final['sold']+df_final['remaining']))

    df_final['ROI']=df_final['profit']/df_final['outflow']*100
    
    
    df_wallet = pd.DataFrame({'buy': [df_final.sum().buy],
    'sell': [df_final.sum().sell],
    'outflow': [df_final.sum().outflow],
    'inflow': [df_final.sum().inflow],
    'salvage': [df_final.sum().salvage],
    'profit': [df_final.sum().inflow + df_final.sum().salvage - df_final.sum().outflow],
    'ROI': [100*(df_final.sum().inflow + df_final.sum().salvage - df_final.sum().outflow)/df_final.sum().outflow]})
    
    
    return(df_wallet,df_final,df_dd)


default_value_goes_here = '0x1dcd52425f559ea602333f28c87f034b27c29526'


user_input = st.text_input("label goes here", default_value_goes_here)



show = uniswap(user_input,df_price,final_price,uniswap_addresses)[1]
st.dataframe(show.sort_values(by=['profit'], ascending = False))

coins1 = show.coin.unique()
coins_plot = st.sidebar.selectbox('Coin',coins1)



ad=uniswap(user_input,df_price,final_price,uniswap_addresses)[2]


filter_coin = coins_plot


close = df_price.loc[df_price['symbol']==filter_coin][['time_h','coin_price']]


close = close.reset_index()


test2 = ad.loc[(ad['symbol']==filter_coin) & (ad['buy']==1)][['buy','time_h']]


test22 = ad.loc[(ad['symbol']==filter_coin) & (ad['sell']==1)][['sell','time_h']]


test3 = close.merge(test2, how = 'left',on=['time_h'])


test4 = test3.merge(test22, how = 'left',on=['time_h'])


states_sell = list(test4.loc[test4['sell']==1].index)


states_buy = list(test4.loc[test4['buy']==1].index)


plt.figure(figsize = (2, 1))
plt.plot(list(test4['time_h']),list(test4['coin_price']), label = 'true close', c = 'g')
plt.plot(list(test4['time_h']),list(test4['coin_price']), 'X', label = 'predict buy', markevery = states_buy, c = 'b')
plt.plot(list(test4['time_h']),list(test4['coin_price']), 'o', label = 'predict sell', markevery = states_sell, c = 'r')
plt.xticks([])
plt.yticks([])
st.pyplot()


show2 = uniswap(user_input,df_price,final_price,uniswap_addresses)[2]
st.dataframe(show2.loc[(show2['symbol']==filter_coin)])





