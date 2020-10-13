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

<p align="center">
  <img src="https://github.com/silkdom/Hidden-Gems/blob/master/img/Etherscan_factory.png?raw=true" alt="uniswap"/>
</p>

Now that the exchnage pair contracts are known, only the transactions that interact with the associated addresses are analyzed. Next step is to identify the user wallet addresses that exchnage with these contracts. This will become our userbase to later narrow down the best traders. At time of writing there were more than 100,000 active wallets. 




### Wallet Analysis
[Price Notebook](y)

[Performance Notebook](z)

Now that that the Uniswap contracts and the users that interact with them are known, the performance of the userbase can be analayzed. However, in order to do this, price data must also be pulled as it is not avaiable via the ethereum tracactional data stream. Thankfully it is an easy pull, via the CoinGecko API. For this project the top 1000 coin hourly price data is deemed sufficient. The time stamps of this price data can be later joined to the tranactional data providing a basis for perfromance analysis. 

The performance mega function combines the data streams and aggregates to both customer/coin and customer levels. This achieved by 




