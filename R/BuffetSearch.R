library(httr)
library(digest)
library(jsonlite)
library(magrittr)
library(stringi)


ACC_KEY <-"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 
ENC_KEY <- "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


##### DATABUFFET SEARCH FUNCTION #####
buffetSearch <- function(query="",start="",rows="", popularitySort="", 
                         ACC_KEY,ENC_KEY){
  
  timeStamp <- format(as.POSIXct(Sys.time()), "%Y-%m-%dT%H:%M:%SZ", tz<-"UTC")
  hashMsg   <- paste(ACC_KEY, timeStamp, sep="")
  signature <- hmac(ENC_KEY, hashMsg, "sha256")
  
  
  query %<>% stri_replace_all_fixed(pattern = " ","%20")
  query %<>% stri_replace_all_fixed(pattern = "|AND|","%20AND%20")
  
  
  
  
  url <- paste("https://api.economy.com/data/v1/search?q=",query,sep="")
  
  
  
  
  if(start != ""){
    url <- paste(url,"&start=",start,sep="")
  }
  
  if(rows != ""){
    url <- paste(url,"&rows=",rows,sep="")
  }
   
  if(popularitySort != ""){
    popularitySort <- ifelse(toupper(popularitySort) == "DESC","long_term_pop%20DESC",popularitySort)
    popularitySort <- ifelse(toupper(popularitySort) == "ASC","long_term_pop%20ASC",popularitySort)  
    url <- paste(url,"&sort=",popularitySort,sep="")
    }
   
  
  
  print(paste("Searching Data Buffet for: ", query, sep=""))
  print(url)
  
  
  Sys.sleep(1)
  req  <- GET(url, 
              add_headers("AccessKeyId"= ACC_KEY,
                          "Signature"  = signature,
                          "TimeStamp"  = timeStamp)
  )
  
  if(req$status_code=="200"){
    print(paste("REQUEST SUCCESSFULL: STATUS CODE",req$status_code,sep = " "))
  }
  else{
    print(paste("REQUEST UNSUCCESSFULL: STATUS CODE",req$status_code,sep = " "))
  }
  
  
  
  searchResults <- req %>% 
    content(as="text") %>%
    fromJSON() %>% 
    extract2("results") %>%
    as.data.frame() 
  
  searchFacets <- req  %>% 
    content(as="text") %>%
    fromJSON() %>% 
    extract2("facets") 
  
  returnList <- list(searchResults,searchFacets)
  names(returnList) <- c("Results","Result_Facets")
  
  return(returnList)
  
}







#########################################################################################################
# Example 1: Search For first 5 results for Manufacturing Employment using DataBuffet's Default sorting
#########################################################################################################
        # Run search 
        mySearch <- buffetSearch(query="manufacturing employment",
                                 start = "0",
                                 rows = "5",
                                 ACC_KEY = ACC_KEY,
                                 ENC_KEY = ENC_KEY)            
            
            # See Search Results 
            results <- mySearch %>% extract2("Results") %>% as.data.frame()
            results %>% View()
            
            
            # View search results by Facet Type:
            #     geo_type, rel_title, geo_title, dms_source, frequency, series_type
            resultFacets <- mySearch %>% extract2("Result_Facets")
            resultFacets %>% names()
            
            # Extract a facet 
            resultFacets %>% 
              extract2("rel_title_exact") %>%
              View()          
            
##########################################################################################
# Example 2: Search For "Employment" where geo_rfa (MA Geo Code) is "IUSA_MPIT"
##########################################################################################            
      mySearch2 <- buffetSearch(query="employment|AND|geo_rfa:IUSA_MPIT",
                                ACC_KEY = ACC_KEY,
                                ENC_KEY = ENC_KEY)
            
            # See Search Results 
            results <- mySearch2 %>% extract2("Results") %>% as.data.frame()
            results %>% View()
            
            
            # View search results by Facet Type:
            #     geo_type, rel_title, geo_title, dms_source, frequency, series_type
            resultFacets <- mySearch2 %>% extract2("Result_Facets")
            resultFacets %>% names()
            
            # Extract a facet 
            resultFacets %>% 
              extract2("rel_title_exact") %>%
              View()               
##########################################################################################
# Example 3: Search for First 100 results of "Employment", sort by descending popularity
##########################################################################################
            # Run Search
            mySearch3 <- buffetSearch(query="employment",
                                     start = "0",
                                     rows = "100",
                                     popularitySort ="desc",
                                     ACC_KEY = ACC_KEY,
                                     ENC_KEY = ENC_KEY)
            
            # See Search Results 
            results <- mySearch3 %>% extract2("Results") %>% as.data.frame()
            results %>% View()
            
            
            # View search results by Facet Type:
            #     geo_type, rel_title, geo_title, dms_source, frequency, series_type
            resultFacets <- mySearch3 %>% extract2("Result_Facets")
            resultFacets %>% names()
            
            # Extract a facet 
            resultFacets %>% 
              extract2("rel_title_exact") %>%
              View()             
            
            
#######################################################################################################                          
# Example 4: Find out what the MA Geo Code for the country/jurisdiction of South Africa is             
#######################################################################################################              

            mySearch4 <- buffetSearch(query="geo_title:South Africa|AND|geo_type_title_exact:Countries/Jurisdictions",
                                      start=0,
                                      rows = 1,
                                      ACC_KEY = ACC_KEY,
                                      ENC_KEY = ENC_KEY) 
            mySearch4 %>% extract2("Results") %>% extract("geo_rfa")
     

            
            
            
            
            
            
            
            
            

            
            
            
            
            
              
              