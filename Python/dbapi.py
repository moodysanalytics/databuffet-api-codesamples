# -*- coding: utf-8 -*-
"""
Library for executing commands via Data Buffet API
https://api.economy.com/data/v1/swagger/ui/index
"""

import os
import json
import datetime
import hmac
import hashlib
import requests
import time
import urllib.parse
import urllib.request
import pandas as pd
import numpy as np
from enum import Enum

class DateOption(Enum):
    StartAndEnd=0
    Start=1
    EntireSeries=2
    Period=3

class BasketFrequency(Enum):
    DEFAULT=0
    DAILY=8
    BUSINESS=9
    WSUN=16
    WMON=17
    WTUE=18
    WWED=19
    WTHU=20
    WFRI=21
    WSAT=22
    MONTHLY=129
    QTROCT=160
    QTRNOV=161
    QTRDEC=162
    QUARTERLY=162
    ANNJAN=192
    ANNFEB=193
    ANNMAR=194
    ANNAPR=195
    ANNMAY=196
    ANNJUN=197
    ANNJUL=198
    ANNAUG=199
    ANNSEP=200
    ANNOCT=201
    ANNNOV=202
    ANNDEC=203
    ANNUAL=203

class DBFileType(Enum):
    Access_ACE12_1Tbl=32
    Access_ACE12_2Tbl=33
    Access_JET4_1Tbl=34
    Access_JET5_2Tbl=35
    Access_3=4
    Access_3_New=5
    Aremos=1
    CSV=12
    CSW_w_Signature_File=95
    EViews=22
    Excel_2=0
    Excel_2000=21
    Excel_2007_2010=30
    HTML=6
    JSON=38
    MA_Dictionary=7
    RFO=76
    Sageworks=81
    Abrigo=81
    Text=3
    MA_Text=2
    XML=13
    TextDat2=8

class BaseAPI:
    def __init__(self,acc_key:str,enc_key:str,oauth:bool = True, proxies=None, debug:bool=False):
        self._base_uri = 'https://api.economy.com'
        self._acc_key = acc_key
        self._enc_key = enc_key
        self._token = 'bearer None'
        self._oauth = oauth
        if proxies is not None:
            self._proxies = proxies
        else:
            self._proxies = urllib.request.getproxies()
        self._debug = debug
        
    def get_oauth_token(self):
        access_key = self._acc_key
        private_key = self._enc_key
        url = f'{self._base_uri}/oauth2/token'
        head = {'Content-Type':'application/x-www-form-urlencoded'}
        data = f'client_id={access_key}&client_secret={private_key}&grant_type=client_credentials'
        r = requests.post(url=url,headers=head,data=data,proxies=self._proxies)
        status = r.status_code
        response = r.text
        jobj = json.loads(response)
        if status == 200:
            return f'{jobj["token_type"]} {jobj["access_token"]}'
        else:
            raise Exception(f'Error - Status : {status}, Msg: {response}')
            
    def get_hmac_header(self):
        timeStamp = datetime.datetime.strftime(
            datetime.datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
        payload = bytes(self._acc_key + timeStamp, "utf-8")
        signature = hmac.new(bytes(self._enc_key,"utf-8"), payload, digestmod=hashlib.sha256)    
        head = {'AccessKeyId':self._acc_key,'Signature':signature.hexdigest(),
                'Content-Type':'application/json','timestamp':timeStamp}
        return head

    def request(self, method:str, url:str, payload={}, max_tries:int=5):
        status = 0
        tries = 0
        ret = {}
        if self._oauth:
            if self._token == 'bearer None':
                self._token = self.get_oauth_token()
        while (not ((status == 200) or ((status == 304) and (method.lower().strip() == "put")))) and (tries < max_tries+1):
            if self._oauth:
                head = {'Authorization':self._token}
            else:
                head = self.get_hmac_header()
            head['Content-Type'] = 'application/json'
            head['Accept'] = 'application/json'
            if method.lower().strip() == "get":
                r = requests.get(url=url,headers=head,proxies=self._proxies)
            elif method.lower().strip() == "post": 
                if type(payload) is list or type(payload) is dict:
                    r = requests.post(url=url,headers=head,json=payload,proxies=self._proxies)
                else:
                    r = requests.post(url=url,headers=head,data=payload,proxies=self._proxies)
            elif method.lower().strip() == "put": 
                if type(payload) is list or type(payload) is dict:
                    r = requests.put(url=url,headers=head,json=payload,proxies=self._proxies)
                else:
                    r = requests.put(url=url,headers=head,data=payload,proxies=self._proxies)
            else:
                print(f'Error - method {method} not recognized')
                return {}
            tries = tries + 1
            status = r.status_code
            response = r.text
            if status == 429:
                print("Too many requests, wait 10 seconds and try again...")
                time.sleep(10)
            elif self._oauth and (status == 401):
                print(self._token,status,response)
                print("Get a new oauth token")
                self._token = self.get_oauth_token()
            elif (status == 200) or ((status == 304) and (method.lower().strip() == "put")):
                try:
                    ret = json.loads(response)
                except ValueError as e:
                    ret = r.content
            else:
                print(f'Error - Status : {status}, Msg : {response}')
                print(f'   URL: {url}')
            if self._debug:
                print(f'{status} : {url}')
        return ret

class DataBuffetAPI(BaseAPI):
    def __init__(self,acc_key:str,enc_key:str,oauth:bool = True,proxies=None,debug:bool=False):
        super().__init__(acc_key,enc_key,oauth,proxies,debug)
        self._base_uri = 'https://api.economy.com/data/v1'
        self._freq_dict = {'DAILY':'D','BUSINESS':'B','BUSINS':'B',\
                           'WSUNDAY':'W-SUN','WSUN':'W-SUN','WMON':'W-MON','WMONDAY':'W-MON','WTUESDAY':'W-TUE','WTUE':'W-TUE','WWEDNESDAY':'W-WED',\
                           'WWED':'W-WED','WTHURSDAY':'W-THU','WTHU':'W-THU','WFRI':'W-FRI','WFRIDAY':'W-FRI','WSAT':'W-SAT','WSATURDAY':'W-SAT',\
                           'BWSUN1':'W-SUN','BWMON1':'W-MON','BWTUE1':'W-TUE','BWWED1':'W-WED','BWTHU1':'W-THU','BWFRI1':'W-FRI','BWSAT1':'W-SAT',\
                           'BWSUN2':'W-SUN','BWMON2':'W-MON','BWTUE2':'W-TUE','BWWED2':'W-WED','BWTHU2':'W-THU','BWFRI2':'W-FRI','BWSAT2':'W-SAT',\
                           'SEMMON':'SM','MONTH':'M','MONTHLY':'M','BIMNOV':'2M','BIMDEC':'2M','QTROCT':'Q-OCT','QTRNOV':'Q-NOV','QTRDEC':'Q-DEC','QUARTERLY':'Q-DEC',\
                           'SEMJUL':'6M','SEMAUG':'6M','SEMSEP':'6M','SEMOCT':'6M','SEMNOV':'6M','SEMIANNUAL':'6M','SEMDEC':'6M',\
                           'ANNJAN':'A-JAN','ANNFEB':'A-FEB','ANNMAR':'A-MAR','ANNAPR':'A-APR','ANNMAY':'A-MAY','ANNJUN':'A-JUN','ANNJUL':'A-JUL',\
                           'ANNAUG':'A-AUG','ANNSEP':'A-SEP','ANNOCT':'A-OCT','ANNNOV':'A-NOV','ANNUAL':'A-DEC','ANNDEC':'A-DEC'}

    def health(self):
        url = f'{self._base_uri}/health'
        ret = self.request(url=url,method="get")
        return ret
    
    def get_series_json(self, mnemonic:str, freq:int=None, transformation:int=None, conversion:int=None, start:str=None, end:str=None, vintage:str=None, vintage_version:int=None):
        url = f'{self._base_uri}/series?m={urllib.parse.quote(mnemonic)}'
        if freq is not None:
            url = f'{url}&freq={freq}'
        if transformation is not None:
            url = f'{url}&trans={transformation}'
        if conversion is not None:
            url = f'{url}&conv={conversion}'
        if start is not None:
            url = f'{url}&startDate={start.strip()}'
        if end is not None:
            url = f'{url}&endDate={end.strip()}'
        if vintage is not None:
            url = f'{url}&vintage={vintage.upper().strip()}'
        if vintage_version is not None:
            url = f'{url}&vintageVersion={vintage_version}'
        ret = self.request(url=url,method="get")
        return ret

    def get_multiseries_json(self, mnemonics:list, freq:int=None, transformation:int=None, conversion:int=None, start:str=None, end:str=None, vintage:str=None, vintage_version:int=None):
        if len(mnemonics) <=25:
            url = f'{self._base_uri}/multi-series?m={urllib.parse.quote(";".join(mnemonics))}'
        else:
            raise Exception('For series lists longer than 25 you must use a basket')
        if freq is not None:
            url = f'{url}&freq={freq}'
        if transformation is not None:
            url = f'{url}&trans={transformation}'
        if conversion is not None:
            url = f'{url}&conv={conversion}'
        if start is not None:
            url = f'{url}&startDate={start.strip()}'
        if end is not None:
            url = f'{url}&endDate={end.strip()}'
        if vintage is not None:
            url = f'{url}&vintage={vintage.upper().strip()}'
        if vintage_version is not None:
            url = f'{url}&vintageVersion={vintage_version}'
        ret = self.request(url=url,method="get")
        return ret
    
    def _to_pandas(self,js:dict):
        index = pd.date_range(freq=self._freq_dict[js['data']['freq']], start=js['data']['startDate'][:10], periods=js['data']['periods'])
        data =  [np.NaN if x == -3.4028234663852886e+38 else x for x in js['data']['data']]
        ret = pd.Series(index=index,data=data)
        ret.mnemonic=js['mnemonic']
        ret.description=js['description']
        ret.source=js['source']
        ret.date_created=pd.to_datetime(js['dateCreated'])
        ret.date_updated=pd.to_datetime(js['dateUpdated'])
        ret.date_accessed=pd.to_datetime(js['dateExecuted'])
        ret.observed=js['observedAttribute']
        ret.geography=js['geoTitle']
        ret.concept=js['concept']
        ret.geo_code=js['geoCode']
        if js['lastHistory'] == 'N/A':
            ret.last_history = None
        else:
            ret.last_history = pd.Period(js['lastHistory'], freq=ret.index.freq ).to_timestamp()
        return ret
        
    def get_series(self, mnemonic:str, freq:int=None, transformation:int=None, conversion:int=None, start:str=None, end:str=None, vintage:str=None, vintage_version:int=None):
        js = self.get_series_json(mnemonic,freq,transformation,conversion,start,end,vintage,vintage_version)
        return self._to_pandas(js)

    def get_multiseries(self, mnemonics:list, freq:int=None, transformation:int=None, conversion:int=None, start:str=None, end:str=None, vintage:str=None, vintage_version:int=None):
        jsons = self.get_multiseries_json(mnemonics,freq,transformation,conversion,start,end,vintage,vintage_version)
        ret = {}
        for js in jsons['data']:
            index = pd.date_range(freq=self._freq_dict[js['freqCode']], start=js['data'][0]['date'], end=js['data'][-1]['date'])
            data =  [np.NaN if x['value'] == -3.4028234663852886e+38 else x['value'] for x in js['data']]
            v = js['mnemonic']
            ret[v]=pd.Series(index=index,data=data)
            ret[v].mnemonic=v
            ret[v].description=js['description']
            ret[v].source=js['source']
            ret[v].observed=js['observedAttribute']
            ret[v].geography=js['geoTitle']
            if js['lastHistory'] == 'N/A':
                ret[v].last_history = None
            else:
                ret[v].last_history = js['lastHistory']
        return ret

    def get_series_vintages(self, mnemonic:str):
        url = f'{self._base_uri}/vintages?m={urllib.parse.quote(mnemonic)}'
        ret = self.request(url=url,method="get")
        return ret
    
    def get_frequencies(self):
        url = f'{self._base_uri}/frequencies'
        ret = self.request(url=url,method="get")
        return ret
    
    def get_baskets_file_types(self):
        url = f'{self._base_uri}/filetypes?type=baskets'
        ret = self.request(url=url,method="get")
        return ret
    
    def get_baskets_list(self, filetype:int=None):
        url = f'{self._base_uri}/baskets'
        if filetype is not None:
            url = f'{url}?filetype={filetype}'
        ret = self.request(url=url,method="get")
        return ret
    
    def get_basket_info(self, basket_id:str):
        url = f'{self._base_uri}/baskets/{basket_id}'
        ret = self.request(url=url,method="get")
        return ret
    
    def get_basket_contents(self, basket_id:str):
        url = f'{self._base_uri}/baskets/{basket_id}/contents'
        ret = self.request(url=url,method="get")
        return ret
    
    def get_basket_output_file(self, basket_id:str, saveto:str=None):
        url = f'{self._base_uri}/baskets/{basket_id}/output-file'
        basket_data = self.request(url=url,method="get")
        if isinstance(basket_data,dict):
            if saveto is not None:
                with open(saveto,'w') as f:
                    f.write(json.dumps(basket_data))
            ret = {}
            for js in basket_data['series']:
                v = js['mnemonic']
                ret[v] = self._to_pandas(js)
            return ret
        else:
            if saveto is not None:
                with open(saveto,'wb') as f:
                    f.write(basket_data)    
            return basket_data
    
    def _basket_option_payload(self, title:str=None, filetype=None, decimals:int=None, start:str=None, end:str=None, date_option=None, frequency=None, showLastHistory:bool=None):
        ret = {}
        ret['options'] = {}
        if title is not None:
            ret['title']=title
        if decimals is not None:
            ret['decimals'] = decimals
        if filetype is not None:
            if isinstance(filetype,int):
                ret['fileTypeId'] = filetype
            if isinstance(filetype,DBFileType):
                ret['fileTypeId'] = filetype.value
        if date_option is not None:
            if isinstance(date_option,int):
                ret['options']['dateOption'] = date_option
            if isinstance(date_option,DateOption):
                ret['options']['dateOption'] = date_option.value
        if frequency is not None:
            if isinstance(frequency,int):
                ret['frequency']=frequency
            if isinstance(frequency,BasketFrequency):
                ret['frequency'] = frequency.value
        else:
            if start is not None:
                if end is not None:
                    ret['options']['dateOption'] = DateOption.StartAndEnd.value
                else:
                    ret['options']['dateOption'] = DateOption.Start.value
        if start is not None:
            ret['dateStart'] = start
        if end is not None:
            ret['dateEnd'] = end
        if showLastHistory is not None:
            ret['options']['showLastHistory'] = showLastHistory
        return ret

    def create_basket(self, title:str, filetype=None, decimals:int=None, start:str=None, end:str=None, date_option=None, frequency=None, showLastHistory:bool=None):
        url = f'{self._base_uri}/baskets'
        pl = self._basket_option_payload(title,filetype)
        ret = self.request(url=url,method="post",payload=pl)
        out = self.edit_basket_settings(basket_id=ret['basketId'],decimals=decimals,start=start,end=end,date_option=date_option,frequency=frequency,showLastHistory=showLastHistory)
        return ret
    
    def edit_basket_settings(self, basket_id:str, title:str=None, filetype=None, decimals:int=None, start:str=None, end:str=None, date_option=None, frequency=None, showLastHistory:bool=None):
        url = f'{self._base_uri}/baskets/{basket_id}'
        pl = self._basket_option_payload(title,filetype,decimals,start,end,date_option,frequency,showLastHistory)
        ret = self.request(url=url,method="post",payload=pl)
        return ret

    def add_series_to_basket(self, basket_id:str, mnemonics:list):
        url = f'{self._base_uri}/baskets/{basket_id}/Series'
        pl = []
        for mnemonic in mnemonics:
            pl.append({'mnemonic':mnemonic})
        ret = self.request(url=url,method="post",payload=pl)
        return ret
    
    def get_orders(self):
        url = f'{self._base_uri}/orders'
        ret = self.request(url=url,method="get")
        return ret
    
    def run_basket(self, basket_id:str):
        url = f'{self._base_uri}/orders?id={basket_id}&type=baskets&action=run'
        ret = self.request(url=url,method="post")
        return ret
    
    def get_order_status(self, order):
        if type(order) is dict:
            order_id = order['orderId']
        else:
            order_id = order
        url = f'{self._base_uri}/orders/{order_id}'
        ret = self.request(url=url,method="get")
        return ret
    
    def wait_for_order(self, order, sleep:int=5):
        status = self.get_order_status(order)
        while status['dateFinished'] is None:
            time.sleep(sleep)
            status = self.get_order_status(order)
        return status
    
    def search(self, query:str, rows:int=30, start:int=0):
        url = f'{self._base_uri}/search?q={urllib.parse.quote(query)}&start={start}&rows={rows}'
        ret = self.request(url=url,method="get")
        return ret