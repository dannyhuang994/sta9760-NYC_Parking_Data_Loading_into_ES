from src.api import get_data
from sys import argv
import argparse
import json

from datetime import datetime
from elasticsearch import Elasticsearch


def create_and_update_index(index_name, doc_type):
    es = Elasticsearch()
    try:
        es.indices.create(index=index_name)
    except Exception:
        pass

    es.indices.put_mapping(
        index=index_name,
        doc_type=doc_type,
        body={
            doc_type: {
                "properties": {"issue_date_time": {"type": "date"},
                }
            }
        }
    )
    return es

def get_output_data(result_fn: str) ->list:
    '''gets data from result_fn and return a list of data points'''
    with open(result_fn) as f_read:
        r = json.load(f_read)
        data_list = r["data_list"]
    return data_list

if __name__=='__main__':
    '''Construct the argument parser to get argument from command line'''  
    ap = argparse.ArgumentParser()
    ap.add_argument("--page_size", type=int, default=None)
    ap.add_argument("--num_pages", type=int, default=None)
    ap.add_argument("--output", default=None)
    args = ap.parse_args()
    page_size, num_pages, output_fn = args.page_size, args.num_pages, args.output

    if page_size is None:
        print('Page size should be specified!')
        exit()

    get_data(page_size, num_pages, output_fn)

    es = create_and_update_index('violation-index', 'violation')
    docks = get_output_data(output_fn)


    ## Push parking violation data into the elastic search
    ## consider dock as a row in the table docks
    i = 0
    if output_fn != None:
        for dock in docks:
            try:
                ## since the value in dock['violation_time'] is 'hh:mmP' or 'hh:mmA' instead of 'hh:mm'+"AM|PM"
                ## we need an extra M to match the pattern
                dock['issue_date_time'] = datetime.strptime(  dock['issue_date'] + ' ' + dock['violation_time']+'M',
                                                        '%m/%d/%Y %I:%M%p' )
            except Exception as e:
                dock['issue_date_time'] = None

            res = es.index(index='violation-index', doc_type='violation', body=dock,)
            print(res['result'] + f' at index: {i}')
            i+=1



