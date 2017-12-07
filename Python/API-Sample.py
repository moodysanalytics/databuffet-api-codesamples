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
  head = {"AccKeyId":accKey, 
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
ENC_KEY = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
ACC_KEY = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
BASKET_NAME = "Test Basket"

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
if order.status_code != 200:
  sleep(3)
  print("Failed! Status Code: "+ str(order.status_code))
else:
  sleep(3)
  print("Successful Order! Status Code: " + str(order.status_code))

# 6. Download completed output.
new_call = ("orders?type=baskets&id=" + basketId)
get_basket = api_call(new_call, ACC_KEY, ENC_KEY)
get_basket = (str(get_basket.content).split("\\r\\n"))

# 7. Format the data frame.
data_df= pd.DataFrame(get_basket)
data_df = data_df[0].str.split(',', expand=True)
headers = data_df.iloc[0]
headers[0] = "Mnemonic"
data_df.columns = headers
data_df = data_df.set_index(data_df["Mnemonic"])
data_df = data_df[:-1]
data_df.dropna(axis=1, how='all')
filter = data_df != ""
data_df = data_df[filter]

# 8. Summary of the data frame.
num_rows = str(len(data_df.index))
num_columns = str(len(data_df.columns))
print("Ready to use "+ BASKET_NAME + " DataFrame!")
print("DataFrame contains: " + num_columns + " columns & " + num_rows + " rows")
