
import requests
import pandas as pd
import json
import time as tt
import numpy as np
import streamlit as st



whale = pd.read_csv("all_users.csv")



metrics = ['profit','ROI','avg_profit','avg_ROI']
sorting = st.radio('Sort by',metrics)

t1 = whale.sort_values(by=[sorting], ascending = False)

no_coins = st.slider('Number of coins', 1, 10, 5)

t2 = t1.loc[t1['no_coins']>no_coins]



no_buys = st.slider('Number of buys', 0, 20, 0)
no_sells = st.slider('Number of sells', 0, 20, 0)

t3 = t2.loc[(t2['buy']>no_buys) & (t2['sell']>no_sells)]
st.dataframe(t3)