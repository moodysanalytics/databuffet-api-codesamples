#####
# Data Buffet API
# Code sample: Python
# Description: Test connection to Data Buffet API

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

def prompt(prompt_text:str):
    ret = None
    while ret is None:
        ret = input(f'{prompt_text} : ').strip()
    return ret

print('\nGet your API heys here: https://economy.com/myeconomy/api-key-info\n')
access_key = prompt('Please enter your access key')
encryption_key = prompt('Please enter your encryption key')

try:
    # instantiate the api class
    api = dbapi.DataBuffetAPI(access_key,encryption_key)

    # check that you are properly connected to API
    health = api.health()
    print(f'API status: {health}')
    if ('SUCCESS' in health.upper()):
        print('[PASS] API successfully accessed')
    else:
        print('[FAIL] Connection health check failed')
except Exception as ex:
    print('[FAIL] Something did not work, see exception below:')
    print(f'Exception : {ex}')