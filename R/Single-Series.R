library(digest)
library(jsonlite)
library(httr)
library(utils)
library(xts)


#####Function that retrieves DataBuffet Series using Mnemonic Code 
#    Frequency & Transformation arguments are optional (see User Guide)
#    Arguments:
#           1. Mnemonic Code 
#           2. Your access key
#           3. Your personal encryption key
#           4. Optional: frequency code (see API User Guide). Default to 0 (Undefined)
#           5. Optional: transformation code (see API User Guide). Default to 0 (Undefined)
get.series <- function(mnemonic, accKey, encKey,freq="0",trans="0"){
  
  apiCommand <- paste("series?m=",utils::URLencode(mnemonic),"&freq=",freq,"&trans=",trans,sep="")
  url <- paste("https://api.economy.com/data/v1/", apiCommand, sep="")
  print(url)
  timeStamp <- format(as.POSIXct(Sys.time()), "%Y-%m-%dT%H:%M:%SZ", tz="UTC")
  hashMsg   <- paste(accKey, timeStamp, sep="")
  signature <- hmac(encKey, hashMsg, "sha256")
  
  Sys.sleep(1)
  req <- httr::GET(url, httr::add_headers("AccessKeyId" = accKey,
                                          "Signature" = signature,
                                          "TimeStamp" = timeStamp))
  #### Are You Behind A Proxy? If so, try:
  #   Add the use_proxy argument to httr::GET 
  #   req <- httr::GET(url, httr::add_headers("AccessKeyId" = accKey,
  #                                           "Signature" = signature,
  #                                           "TimeStamp" = timeStamp),
  #                  use_proxy("http:://myproxy",80))
  # if required to ignore ssl certs
  # response <- GET("https://example.com", config(ssl_verifypeer = FALSE))
  series <- jsonlite::fromJSON(httr::content(req, as="text"))
  return(series)
}

#####
# Setup:
# 1. Store your access key, encryption key.
# Get your keys at:
# https://www.economy.com/myeconomy/api-key-info
ACC_KEY  <- "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
ENC_KEY  <- "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"

##### Example 1: 
myData <- get.series("ET.IUSA",ACC_KEY,ENC_KEY)


##### Optionally, turn the series into an xts object: 
#   dates <- seq(from=as.Date(myData$startDate),to=as.Date(myData$endDate),
#             length.out = myData$data$periods) 
#   xts_data <- xts(as.numeric(myData$data$data),dates)
