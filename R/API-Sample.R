#####
# Data Buffet API
# Code sample: R
# 1 December 2017
# (c)2017 Moody's Analytics

library(digest)
library(jsonlite)
library(httr)

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
# httr content object
api.call <- function(apiCommand, accKey, encKey, type="GET"){
  url <- paste("https://api.economy.com/data/v1/", apiCommand, sep="")
  print(url)
  timeStamp <- format(as.POSIXct(Sys.time()), "%Y-%m-%dT%H:%M:%SZ", tz="UTC")
  hashMsg   <- paste(accKey, timeStamp, sep="")
  signature <- hmac(encKey, hashMsg, "sha256")
  
  Sys.sleep(1)
  if (type == "POST") {
    req <- httr::POST(url, httr::add_headers("AccessKeyId" = accKey,
                                             "Signature" = signature,
                                             "TimeStamp" = timeStamp))
  } else {
    req <- httr::GET(url, httr::add_headers("AccessKeyId" = accKey,
                                            "Signature" = signature,
                                            "TimeStamp" = timeStamp))
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

#####
# Identify a basket to execute:
# 2. Get list of baskets.
# 3. Extract the basket with a given name, and save its ID for later.
baskets.json <- api.call("baskets/", ACC_KEY, ENC_KEY)
baskets      <- fromJSON(httr::content(baskets.json, as="text"))
basketID     <- baskets$basketId[baskets$name==BASKET_NAME]

# 4. Execute a particular basket using its ID.
# This requires that the optional argument “type” be set to "POST".
call    <- paste("orders?type=baskets&action=run&id=", basketID, sep="")
order   <- api.call(call, ACC_KEY, ENC_KEY, type="POST")
orderID <- fromJSON(httr::content(order, as="text"))$orderId

#####
# Download the output:
# 5. Periodically check if the order has completed.
call <- paste("orders/", orderID, sep="")
processing.check <- TRUE
while(processing.check) {
  status <- api.call(call, ACC_KEY, ENC_KEY)
  processing.check <- fromJSON(httr::content(status, as="text"))$processing
  Sys.sleep(10)
}
rm(status)

# 6. Download completed output.
call    <- paste("orders?type=baskets&id=", basketID, sep="")
request <- api.call(call, ACC_KEY, ENC_KEY)

# 7. This works for CSV baskets:
cat(httr::content(request, as="text", type="text/html", encoding="UTF-8"),
    file="basket.data", sep="\n")
df_data <- as.data.frame(read.csv("basket.data"))

# 8. View the data.
View(df_data)

# 9. Clean up.
unlink("basket.data")
rm(ACC_KEY, ENC_KEY)
rm(baskets, basketID, baskets.json)
rm(order, orderID)
rm(processing.check, call, request)