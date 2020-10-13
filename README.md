# Hidden-Gems
## Overview

Wouldn't it be great if you could follow the moves of the world's best equity market trader in real time, akin to being Warren Buffet's shadow. However, this is obviously not possible due to the opaqueness of such markets. With crypto markets this is also challenging as centralized exchanges generally deal with 'paper' assets meaning that internal transactions occur on their scaled network reather than assset's blockchain (Btc, Eth, etc.), thus rendering the tracking of an individuals returns very challenging. 

This is where decentralized finance (or defi) comes into play. What is defi? read here... [CoinDesk article](https://www.coindesk.com/what-is-defi)
Uniswap is the most prominant dapp and main facilitator of the recent explosive growth seen in the space. It's main role is a decentralized exchange, where market participants can trade or provide liquidity to erc-20 tokens. Conversly to equity, or conventional crypto markets, all transactions are visable on the ethereum blockchain. 

The transpacerency of the ecosystem blossomed the idea of an app that could find the wallets of the biggest winners (via a vareity of metrics), and provide a tracking functionality of such addresses. The resulting insights can facilitate the following profit generating activities; copy trading, smart-money sentiment analysis, and hidden gem (low mcap project) disovery. This repo outlines how these outcomes are achived through the creation of two interactable python web apps and a heroku deployed telegram bot. 

<p align="center">
  <img src="https://github.com/silkdom/Hidden-Gems/blob/master/img/uniswap.png?raw=true" height="400" alt="uniswap"/>
</p>


## How it Works

The workflow for the generation of tattoo design ideas can be broken into 3 sections;

- Wallet Identification
- Wallet Analysis
- Wallet Tracking

Data is sourced from the Etherscan and CoinGecko Api's. Periodic sleep functions are implemented to abide by their rate call limits. Documentation can be found here; [Etherscan](https://etherscan.io/apis), [CoinGecko](https://www.coingecko.com/en/api)

### Wallet Identification
[Contract & Address Notebook](x)

In order to determine a traders performance it is neccisary to see if they are buying/selling coins, or just moving them to another wallet on the blockchain. This can be done by identifying the token contracts used for exchange on the Uniswap protocal. These contracts were initially difficult to compile, but thankfully could be determined from the logs of the Uniswap factory contract. At time of writing there were 13,344 unique exchange pairs.

```python
# Run if want fresh listings

factory = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
topic0 = '0x0d3648bd0f6ba80134a33ba9275ac585d9d315f0ad8355cddefde31afa28d0e9'
blockchain = list(range(10000000,11100000,10000))
# last block on last run --- August 15th ~ 10620088
uniswap_addresses = []

for block in blockchain:
    block2 = str(block+10000)
    block1 = str(block)
    print(block)
    tt.sleep(3)
    
    call = 'https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock='+block1+'&toBlock='+block2+'&address='+factory+'&topic0='+topic0+'&apikey=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    response = requests.get(call)
    logs = response.json()
    
    addresses = []
    for log in range(len(logs['result'])):
        addresses.append(logs['result'][log]['data'])
    
    addresses2 = []
    for a in range(len(addresses)):
        s = '0x'+addresses[a][26:]
        addresses2.append(s)
    
    addresses3 = []
    for a in range(len(addresses2)):
        s = addresses2[a][:-64]
        addresses3.append(s)
    
    uniswap_addresses.extend(addresses3)
```

Now that the exchnage pair contracts are known, only the transactions that interact with the associated addresses are analyzed. Next step is to identify the user wallet addresses that exchnage with these contracts. This will become our userbase to later narrow down the best traders. At time of writing there were more than 100,000 active wallets. 

```python
# Run if want fresh user wallet addresses

wallet_addresses = []
k = 0
j = 0
for u in uniswap['0']:
    if k % 8 ==0:
        tt.sleep(1)
    k += 1
    print(k)
    
    try:
        wallets = requests.get('http://api.etherscan.io/api?module=account&action=tokentx&address='+u+'&startblock=0&endblock=999999999&sort=asc&apikey=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        wallets = wallets.json()

        addresses = []
        for i in range(len(wallets['result'])):
            addresses.append(wallets['result'][i]['to'])
            addresses.append(wallets['result'][i]['from'])

        wallet_addresses.extend(addresses)
        wallet_addresses = list(set(wallet_addresses))
        
    except:
        j += 1
        print('Error #'+str(j))
        pass
```

### Wallet Analysis
[Price Notebook](y)

[Performance Notebook](z)

Now that that the Uniswap contracts and the users that interact with them are known, the performance of the userbase can be analayzed. However, in order to do this, price data must also be pulled as it is not avaiable via the ethereum tracactional data stream. Thankfully it is an easy pull, via the CoinGecko API. For this project the top 1000 coin hourly price data is deemed sufficient. The time stamps of this price data can be later joined to the tranactional data providing a basis for perfromance analysis. 

The performance mega function, uniswap() combines the data streams and aggregates to both customer/coin and customer levels. This achieved by first using the Etherscan API to pull all of the addresses ERC-20 token transactions. These transactions are then compared to the contract addresses above to detrmine if the transaction was an exchange on the uniswap portocall ('to' = sell, 'from' = buy). The price data is then merged to the transactions on the rounded (to nearest hour) timestamps and coin ticker (i.e. Btc, Eth, etc.). Metrics such as inventory, remaining, and salvage are introduced to ensure that performance can be assessed legitimately over the blockchain snapshot. The transactions are then aggregated by coin ticker, and evaluation metrics such as profit and ROI are computed on a coin basis. The aggregation is then done again on a total portfolio basis, and the two perfomance tables are returned from the function. 

```python
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
```

We can now apply the function to the addresses of the Uniswap protocall. So that no stone is left unturned, all 100,000+ users are ran through the function, and their high level performance metrics are recorded. The final part of the project, is to dive deeper into the biggest winners identified in this section, and develop a method to tracking their future transactions. 

### Wallet Tracking

[Interactive Tracking #1](https://github.com/silkdom/Hidden-Gems/blob/master/Whale-Watching/Etherscan_app_function.py)

[Interactive Tracking #2](https://github.com/silkdom/Hidden-Gems/blob/master/Whale-Watching/whale_hunt.py)

[Telegram Bot](https://github.com/silkdom/Hidden-Gems/blob/master/heroku.py)
