#####
# Data Buffet API
# Code sample: Python
# 1 December 2017
# (c)2017 Moody's Analytics
 
import requests
import hashlib 
import hmac
import datetime
import json
import pandas as pd
from time import sleep
from io import BytesIO
import binascii

#####
# Function: Make API request, including a freshly generated signature.
#
# Arguments:
# 1. Part of the endpoint, i.e., the URL after "https://api.economy.com/data/v1/"
# 2. Your access key.
# 3. Your personal encryption key.
# 4. Optional: default GET, but specify POST when requesting action from the API.
#
# Returns:
# HTTP response object.
def api_call(apiCommand, accKey, encKey, call_type="GET"):
  url = "https://api.economy.com/data/v1/" + apiCommand
  timeStamp = datetime.datetime.strftime(
    datetime.datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
  payload = bytes(accKey + timeStamp, "utf-8")
  signature = hmac.new(bytes(encKey, "utf-8"), payload, digestmod=hashlib.sha256)
  head = {"AccessKeyId":accKey, 
          "Signature":signature.hexdigest(), 
          "TimeStamp":timeStamp}
  sleep(1)
  if call_type == "POST":
    response = requests.post(url, headers=head)
  elif call_type =="DELETE":
    response = requests.delete(url, headers=head)
  else:
    response = requests.get(url, headers=head)
    
  return(response)

#####
# Setup:
# 1. Store your access key, encryption key, and basket name.
# Get your keys at:
# https://www.economy.com/myeconomy/api-key-info
ACC_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
ENC_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
BASKET_NAME = "TEST BASKET NAME"

#####
# Identify a basket to execute:
# 2. Get list of baskets.
# 3. Extract the basket with a given name, and save its ID for later.
baskets = pd.DataFrame(json.loads(api_call("baskets/", ACC_KEY, ENC_KEY).text))
basketId = baskets.loc[baskets["name"]==BASKET_NAME, "basketId"].item()
print("Basket ID: " + basketId)
print("Basket Name: " + BASKET_NAME)

# 4. Execute a particular basket using its ID.
# This requires that the optional argument "type" be set to "POST".
call = ("orders?type=baskets&action=run&id=" + basketId)
order = api_call(call, ACC_KEY, ENC_KEY, call_type="POST")
orderId = order.text[12:48]
print("Order ID: " + orderId)

#####
# Download the output:
# 5. Periodically check if the order has completed.
call = "orders/" + orderId
processing_check = True
while processing_check:
    sleep(5)
    status = api_call(call, ACC_KEY, ENC_KEY)
    processing_check = json.loads(status.content.decode('utf-8'))['processing']
    print('processing: ' + str(processing_check))  
  
  
# 6. Download completed output.
new_call = ("orders?type=baskets&id=" + basketId)
get_basket = api_call(new_call, ACC_KEY, ENC_KEY)

## Choose one from below two line of codes:
get_basket = (str(get_basket.content).split("\\r\\n"))   ## This line of code for csv files
get_basket = pd.read_excel(BytesIO(get_basket.content))  ## This line of code for xlsx files

# 7. Format the data frame.
data_df= pd.DataFrame(get_basket)
data_df = data_df[0].str.split(',', expand=True)
headers = data_df.iloc[0]
data_df.dropna(axis=1, how='all')
filter = data_df != ""
data_df = data_df[filter]

# 8. Summary of the data frame.
num_rows = str(len(data_df.index))
num_columns = str(len(data_df.columns))
print("Ready to use "+ BASKET_NAME + " DataFrame!")
print("DataFrame contains: " + num_columns + " columns & " + num_rows + " rows")
