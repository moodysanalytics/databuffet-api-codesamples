# Data Buffet API v1 Code Samples

## Introduction

Data Buffet (DataBuffet.com) is the Moody's Analytics repository of international and subnational economic and demographic time series data. We provide several means of manual and automatic access that you can integrate with your workflow, among them, the Data Buffet API (application program interface). The API uses HMAC authentication and JSON responses, and is agnostic regarding the client's operating system and programming language. The API is throttled (rate-limited) to one request per second and one gigabyte of data per month.

The code samples in this GitHub repository provide a starting point to write your custom software solutions to retrieve individual series or baskets via the API. There are four languages: C#, Java, Python and R. The first two languages are projects (multiple files in a folder structure) that can be opened in an IDE (Microsoft Visual Studio and Eclipse, respectively); the latter two are single source files. The content of the samples, and the set of languages, are subject to change.

Please see documentation [here](https://github.com/moodysanalytics/databuffet.api.codesamples/blob/master/databuffet-api-userguide.pdf).


## Prerequisites

* A subscription to the DataBuffet.com web site.
* Basic training in the contents and use of time series retrievable via DataBuffet.com.
* Any operating system.
* An appropriate development environment for your OS, for one or more of C#, Java, Python or R.
* Basic familiarity with the concepts of a web service API (our user guide PDF can get you started).

## Contents of this repository

* C#: for Microsoft Visual Studio, with .sln "solutions" file to build "APICodeSample"
* Java: for Eclipse, with .iml "IntelliJ module" file to build "API Java Code Sample"
* Python: 
  * dbapi.py : Class that implements Data Buffet API
  * _test_dbapi_on_my_system.py : Tests connection from your network to Data Buffet API
  * dbapi_create_and_run_basket.py : Sample code to create, run, and download a basket
* R: API-Sample.R
* User guide PDF: databuffet-api-userguide.pdf
* Enumerations for frequency, transformation, conversion type, and date options

## Support and contributions

Please contact the Data Buffet API team at Moody's Analytics at either:
* https://www.economy.com/about/contact-us with Topic set to "technical inquiry"
* By email at helpeconomy@moodys.com, with a Subject line of "Data Buffet API technical inquiry"

## License

(c) 2024 Moody's Analytics, Inc. All rights reserved.
