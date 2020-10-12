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

### Wallet Identification
[Notebook](https://github.com/silkdom/Hidden-Gems/blob/master/Whale-Watching/Etherscan_app_function.py)

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
    
    call = 'https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock='+block1+'&toBlock='+block2+'&address='+factory+'&topic0='+topic0+'&apikey='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
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
        wallets = requests.get('http://api.etherscan.io/api?module=account&action=tokentx&address='+u+'&startblock=0&endblock=999999999&sort=asc&apikey=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
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
