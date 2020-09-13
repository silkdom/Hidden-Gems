#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import time as tt
import pandas as pd
from  os import environ


# In[42]:
apikey = environ['apikey']

def telegram_bot_sendtext(bot_message):


   bot_token = environ['bot_token']
   bot_chatID = environ['bot_chatID']
   
   
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

   response = requests.get(send_text)

   return response.json()


# In[4]:


whales = pd.read_csv('whales.csv')


# In[11]:


block1 = 10150000
block2 = 10783345#99999999

address = whales['address'][0]


# In[15]:


def ad(block1,block2,address):
    call = 'https://api.etherscan.io/api?module=account&action=tokentx&address='+address+'&startblock='+str(block1)+'&endblock='+str(block2)+'&sort=asc&apikey='+apikey
    response = requests.get(call)
    txns = response.json()
    return(txns)


# In[22]:


whales['lastblock']=1
whales['freq']=0
for i in range(len(whales)):
    tt.sleep(1)
    a = ad(block1,block2,whales['address'][i])
    whales['lastblock'][i]=a['result'][-1]['blockNumber']
    print(i)


# In[ ]:


cnt = 0
while cnt < 3000:
    cnt += 1
    tt.sleep(30)
    print(cnt)
    for index, row in whales.iterrows():
        tt.sleep(3)
        try:
            c = ad(row.lastblock+1,99999999,row.address)
        except:
            print('Error')
            continue
        
        if c['status'] == '0':
            continue
            
        else:
            whales.at[index,'lastblock'] = int(c['result'][-1]['blockNumber'])
            whales.at[index,'freq'] = row.freq+1
        
        bs = 'none'        
        if row.address == c['result'][-1]['to']:
            bs = 'bought'+u'\U0001F34F'  
        elif row.address == c['result'][-1]['from']:
            bs = 'sold'+u'\U0001F34E'
    
        tkn = 'none'
        tkn = c['result'][-1]['tokenName']
        
        sym = 'none'
        sym = c['result'][-1]['tokenSymbol']
        
        amt = 0
        amt = round(float(c['result'][-1]['value'])/(10**(float(c['result'][-1]['tokenDecimal']))),2)
        
        add = 'none'
        add = row.address
        
        freq = 'none'
        freq = str(row.freq+1)
        
        message = telegram_bot_sendtext(add+" [[]"+freq+"[]] "+" Activity: "+bs+" "+str(amt)+" of "+tkn+", "+"[[]"+sym+"[]]")

