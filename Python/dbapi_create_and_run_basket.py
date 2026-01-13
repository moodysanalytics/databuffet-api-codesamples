#####
# Data Buffet API
# Code sample: Python
# Description: Create, execute, and download basket

import sys
import os
try:
    import dbapi
except Exception as ex:
    print(ex)
    print('Make sure dbapi.py is downloaded to the same directory as this program, and run again')
    print('Get it here: https://github.com/moodysanalytics/databuffet-api-codesamples/blob/master/Python/dbapi.py')
    sys.exit()
import pandas as pd
import numpy as np
from datetime import datetime

def prompt(prompt_text:str):
    ret = None
    while ret is None:
        ret = input(f'{prompt_text} : ').strip()
    return ret

print('\nGet your API heys here: https://economy.com/myeconomy/api-key-info\n')
access_key = prompt('Please enter your access key')
encryption_key = prompt('Please enter your encryption key')

# instantiate the api class
api = dbapi.DataBuffetAPI(access_key,encryption_key)

# locate available series to test with
search = api.search(query='SA',rows=2)
series_list = [x['mnemonic'] for x in search['results']]
print(f'Downloading : {series_list}')

# Create and basket for the series
basket = api.create_basket('API_BASKET_'+datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f'),filetype=dbapi.DBFileType.JSON)
basket_id = basket['basketId']
basket_name = basket['basketName']
print(f'created basket at : https://www.economy.com/databuffet/preview/basket/{basket_id}')

# Run the basket
api.add_series_to_basket(basket_id,series_list)
order = api.run_basket(basket_id)
api.wait_for_order(order)

# Download the data to disk, and put results in dictionary of pandas series (my_basket_data)
my_basket_data = api.get_basket_output_file(basket_id, saveto=f'{basket_name}.json')
print(f'Basket data file written to {os.getcwd()}\\{basket_name}.json')