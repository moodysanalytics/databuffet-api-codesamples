#####
# Data Buffet API
# Code sample: R
# 1 December 2017
# (c)2017 Moody's Analytics

library(jsonlite)
library(httr)

#####
# Function: Fetch an OAuth 2.0 bearer token. Fetch it once and reuse it for
# the session; tokens are valid for one hour.
#
# Arguments:
# 1. Your access key (used as the OAuth client_id).
# 2. Your personal encryption key (used as the OAuth client_secret).
#
# Returns:
# The access token string (pass it to api.call).
get.oauth.token <- function(accKey, encKey){
  url  <- "https://api.economy.com/data/v1/oauth2/token"
  body <- list(client_id     = accKey,
               client_secret = encKey,
               grant_type    = "client_credentials")
  req   <- httr::POST(url, body=body, encode="form")
  token <- jsonlite::fromJSON(httr::content(req, as="text"))
  return(token$access_token)
}

#####
# Function: Make API request, authenticating with an OAuth 2.0 bearer token.
#
# Arguments:
# 1. Part of the endpoint, i.e., the URL after "https://api.economy.com/data/v1/"
# 2. Your OAuth bearer token (from get.oauth.token).
# 3. Optional: default GET, but specify POST when requesting action from the API.
#
# Returns:
# httr content object
api.call <- function(apiCommand, token, type="GET"){
  url <- paste("https://api.economy.com/data/v1/", apiCommand, sep="")
  print(url)

  Sys.sleep(1)
  if (type == "POST") {
    req <- httr::POST(url, httr::add_headers("Authorization" = paste("Bearer", token)))
  } else {
    req <- httr::GET(url, httr::add_headers("Authorization" = paste("Bearer", token)))
  }
  return(req)
}

#####
# Setup:
# 1. Store your access key, encryption key, and basket name.
# Get your keys at:
# https://www.economy.com/myeconomy/api-key-info
ACC_KEY     <- "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
ENC_KEY     <- "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
BASKET_NAME <- "Test Basket"

# Fetch an OAuth token once and reuse it for every request below.
TOKEN <- get.oauth.token(ACC_KEY, ENC_KEY)

#####
# Identify a basket to execute:
# 2. Get list of baskets.
# 3. Extract the basket with a given name, and save its ID for later.
baskets.json <- api.call("baskets/", TOKEN)
baskets      <- fromJSON(httr::content(baskets.json, as="text"))
basketID     <- baskets$basketId[baskets$name==BASKET_NAME]

# 4. Execute a particular basket using its ID.
# This requires that the optional argument “type” be set to "POST".
call    <- paste("orders?type=baskets&action=run&id=", basketID, sep="")
order   <- api.call(call, TOKEN, type="POST")
orderID <- fromJSON(httr::content(order, as="text"))$orderId

#####
# Download the output:
# 5. Periodically check if the order has completed.
call <- paste("orders/", orderID, sep="")
processing.check <- TRUE
while(processing.check) {
  status <- api.call(call, TOKEN)
  processing.check <- fromJSON(httr::content(status, as="text"))$processing
  Sys.sleep(10)
}
rm(status)

# 6. Download completed output.
call    <- paste("orders?type=baskets&id=", basketID, sep="")
request <- api.call(call, TOKEN)

# 7. This works for CSV baskets:
cat(httr::content(request, as="text", type="text/html", encoding="UTF-8"),
    file="basket.data", sep="\n")
df_data <- as.data.frame(read.csv("basket.data"))

# 8. View the data.
View(df_data)

# 9. Clean up.
unlink("basket.data")
rm(ACC_KEY, ENC_KEY, TOKEN)
rm(baskets, basketID, baskets.json)
rm(order, orderID)
rm(processing.check, call, request)