#####
# Data Buffet API
# Code sample: Python
# 1 December 2017
# (c)2017 Moody's Analytics
 
import requests
import json
import pandas as pd
from time import sleep
from io import BytesIO

#####
# Function: Fetch an OAuth 2.0 bearer token. Fetch it once and reuse it for
# the session; tokens are valid for one hour.
#
# Arguments:
# 1. Your access key (used as the OAuth client_id).
# 2. Your personal encryption key (used as the OAuth client_secret).
#
# Returns:
# The access token string (pass it to api_call).
def get_oauth_token(accKey, encKey):
  url = "https://api.economy.com/data/v1/oauth2/token"
  head = {"Content-Type": "application/x-www-form-urlencoded"}
  data = ("client_id=" + accKey +
          "&client_secret=" + encKey +
          "&grant_type=client_credentials")
  response = requests.post(url, headers=head, data=data)
  if response.status_code != 200:
    raise Exception("Error fetching OAuth token - Status: " +
                    str(response.status_code) + ", Msg: " + response.text)
  return json.loads(response.text)["access_token"]

#####
# Function: Make API request, authenticating with an OAuth 2.0 bearer token.
#
# Arguments:
# 1. Part of the endpoint, i.e., the URL after "https://api.economy.com/data/v1/"
# 2. Your OAuth bearer token (from get_oauth_token).
# 3. Optional: default GET, but specify POST when requesting action from the API.
#
# Returns:
# HTTP response object.
def api_call(apiCommand, token, call_type="GET"):
  url = "https://api.economy.com/data/v1/" + apiCommand
  head = {"Authorization": "Bearer " + token}
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

# Fetch an OAuth token once and reuse it for every request below.
TOKEN = get_oauth_token(ACC_KEY, ENC_KEY)

#####
# Identify a basket to execute:
# 2. Get list of baskets.
# 3. Extract the basket with a given name, and save its ID for later.
baskets = pd.DataFrame(json.loads(api_call("baskets/", TOKEN).text))
basketId = baskets.loc[baskets["name"]==BASKET_NAME, "basketId"].item()
print("Basket ID: " + basketId)
print("Basket Name: " + BASKET_NAME)

# 4. Execute a particular basket using its ID.
# This requires that the optional argument "type" be set to "POST".
call = ("orders?type=baskets&action=run&id=" + basketId)
order = api_call(call, TOKEN, call_type="POST")
orderId = order.text[12:48]
print("Order ID: " + orderId)

#####
# Download the output:
# 5. Periodically check if the order has completed.
call = "orders/" + orderId
processing_check = True
while processing_check:
    sleep(5)
    status = api_call(call, TOKEN)
    processing_check = json.loads(status.content.decode('utf-8'))['processing']
    print('processing: ' + str(processing_check))  
  
  
# 6. Download completed output.
new_call = ("orders?type=baskets&id=" + basketId)
get_basket = api_call(new_call, TOKEN)

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
