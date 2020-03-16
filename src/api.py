from requests import get, HTTPError
from sodapy import Socrata
from src.dataCount import get_size
import os
import json

API_BASE = 'data.cityofnewyork.us'
END_POINT = 'nc67-uf89'
APP_KEY = os.environ.get('APP_KEY')

def text_to_float(string1: str):
    ''' this changes a string input which was read as string but actually numeric'''
    try: 
        return float(string1)
    except Exception as e:
        return None

def get_data(page_size: int, num_pages = None, output_fn = None):
    ''' get the data from API,
        either save the data into output_fn or print when output_fn is not provided.
        when num_pages is not specified, we will continue reading data until the end of database'''
    if num_pages is None:
        total = get_size(API_BASE,END_POINT,APP_KEY )
        num_pages = (total // page_size) + 1

    try:
        client = Socrata(API_BASE, APP_KEY)
    except HTTPError as e:
        print(f'Check URL: {e}')
        raise
    except Exception as e:
        print(f'Something Went Wrong: {e}')
        raise

    try:
        if output_fn is None:
            for i in range(num_pages):
                r = client.get(END_POINT, limit = page_size, offset = i*page_size)
                for item in r:
                    print(item)
        else:
            with open(output_fn, 'w') as fw:
                temp = {'Number of Records': page_size*num_pages,'data_list':[]}
                for i in range(num_pages):
                    r = client.get(END_POINT, limit = page_size, offset = i*page_size)
                    for item in r:
                        item['amount_due'] = text_to_float(item.get('amount_due'))
                        item['fine_amount'] = text_to_float(item.get('fine_amount'))
                        item['interest_amount'] = text_to_float(item.get('interest_amount'))
                        item['payment_amount'] = text_to_float(item.get('payment_amount'))
                        item['penalty_amount'] = text_to_float(item.get('penalty_amount'))                
                        item['reduction_amount'] = text_to_float(item.get('reduction_amount'))

                        temp['data_list'].append(item)
                json.dump(temp, fw)
    except Exception as e:
        print(f'Something Went Wrong with: {e}')
        raise

