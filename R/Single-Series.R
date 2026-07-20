library(jsonlite)
library(httr)
library(utils)
library(xts)


#####Function that fetches an OAuth 2.0 bearer token.
#    Fetch it once and reuse it for the session; tokens are valid for one hour.
#    Arguments:
#           1. Your access key (used as the OAuth client_id)
#           2. Your personal encryption key (used as the OAuth client_secret)
#    Returns: the access token string (pass it to get.series)
get.oauth.token <- function(accKey, encKey){
  url  <- "https://api.economy.com/data/v1/oauth2/token"
  body <- list(client_id     = accKey,
               client_secret = encKey,
               grant_type    = "client_credentials")
  req   <- httr::POST(url, body=body, encode="form")
  token <- jsonlite::fromJSON(httr::content(req, as="text"))
  return(token$access_token)
}

#####Function that retrieves DataBuffet Series using Mnemonic Code
#    Frequency & Transformation arguments are optional (see User Guide)
#    Arguments:
#           1. Mnemonic Code
#           2. Your OAuth bearer token (from get.oauth.token)
#           3. Optional: frequency code (see API User Guide). Default to 0 (Undefined)
#           4. Optional: transformation code (see API User Guide). Default to 0 (Undefined)
get.series <- function(mnemonic, token,freq="0",trans="0"){

  apiCommand <- paste("series?m=",utils::URLencode(mnemonic),"&freq=",freq,"&trans=",trans,sep="")
  url <- paste("https://api.economy.com/data/v1/", apiCommand, sep="")
  print(url)

  Sys.sleep(1)
  req <- httr::GET(url, httr::add_headers("Authorization" = paste("Bearer", token)))
  #### Are You Behind A Proxy? If so, try:
  #   Add the use_proxy argument to httr::GET
  #   req <- httr::GET(url, httr::add_headers("Authorization" = paste("Bearer", token)),
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

# Fetch an OAuth token once and reuse it for every request below.
TOKEN <- get.oauth.token(ACC_KEY, ENC_KEY)

##### Example 1:
myData <- get.series("ET.IUSA",TOKEN)


##### Optionally, turn the series into an xts object: 
#   dates <- seq(from=as.Date(myData$startDate),to=as.Date(myData$endDate),
#             length.out = myData$data$periods) 
#   xts_data <- xts(as.numeric(myData$data$data),dates)
