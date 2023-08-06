import math
import os
import requests
from typing import Any
import time

import numpy as np
from pandas.core.frame import DataFrame
import pandas as pd

from progress_keeper import Progress


def timer(func) -> Any:
    """
    Decorator used to time a function call.  After function is run, the time
    of the function call will be outputed as a print statement.
    """
    def f(*args, **kwargs):
        before = time.time()
        rv = func(*args, **kwargs)
        after = time.time()
        print(f'{func.__name__} took {after-before:.2f} seconds.')
        return rv
    return f


def create_api_request_str(vars, state_code,
                           request_url_pre,
                           request_url_post_1, request_url_post_2,
                           api_key) -> str:
    """
    Create api request string by injecting the 'vars' and US state code into the 
    appropriate place within the string.
    
    Args:
        vars (List(str)): list of demographic variables 
        state_code (str): US state code
        request_url_pre (str): beginning part api request url 
        request_url_post_1 (str): api request middle bit of string
        request_url_post_2 (str): api request middle bit of string
        api_key (str): api key
        
    Returns: 
        str: complete api request url string.
    """

    request_variables = ''
    for var in vars:
        if request_variables == '':
            request_variables = var
        else:
            request_variables = request_variables + ',' + var

    return request_url_pre + request_variables + request_url_post_1 + \
        state_code + request_url_post_2 + api_key


@timer
def api_extract_batch(vars, request, retries=5) -> DataFrame:
    """
    Extract one json batch of demographic variables from the US census api using the 
    'request' url.  Parse json response into a dataframe. 
    
    Args:
        vars (List(str)): list of demographic vars that matches the vars injected 
            into the 'request' url
        request (str): request url
        retries (int): number of times to retry the api call if a request was 
            unsuccessful
        
    Returns:
        results_df (Dataframe): results extracted from the json response for the 
            api batch call
    
    Raises: 
        Exception: if api request fails 
    
    """
    # create containers to hold requested data
    data = {}
    tract = []
    county = []
    state = []

    exception = ""

    # request data from API
    for attempt in range(retries):
        try:
            r = requests.get(request)
            if r.status_code == 200:
                for k in r.json():
                    # Census Tract GEOID: STATE+COUNTY+TRACT (2+3+6 digits)
                    tract.append(k[len(k) - 3] + k[len(k) - 2] + k[len(k) - 1])
                    county.append(k[len(k) - 2])
                    state.append(k[len(k) - 3])
                    # start with the second piece of json data, first piece is not needed
                    json_data_index = 1
                    for var in vars:
                        if var not in data:
                            data[var] = []
                        data[var].append(k[json_data_index])
                        json_data_index = json_data_index + 1
            else:
                print(
                    f'REQUEST FAILED ON STATUS CODE: {r.status_code}, Attempt {str(attempt+1)}, {request}')
        except Exception as x:
            print(f'BAD REQUEST: {type(x)} {x} {request}')
            exception = x
            # wait incrementally longer each retry
            wait_time = 30 * (attempt+1)**2
            print(f'Waiting {wait_time} seconds.')
            time.sleep(wait_time)
        else:
            break
    else:
        # all attempts failed, log this
        print(
            f'API REQUEST FAILED AFTER {retries} ATTEMPTS WITH EXCEPTION: {exception} :: {request}')
        empty_result = pd.DataFrame()
        return empty_result

    result_df = pd.DataFrame(data, index=tract)
    result_df['county'] = county
    result_df['state'] = state 
    result_df.index.names = ['census_tract_geoid']
    result_df = result_df[1:]

    return result_df


def api_state_extract(num_processed, num_to_process,
                      vars, state_code,
                      request_url_pre, request_url_post_1, request_url_post_2, api_key) -> DataFrame:
    """
    Generator that wraps api_extract_batch and yields the results. 

    Args:
        num_processed (int): number of batches processed
        num_to_process (int): total number of batches to process
        vars (List(str)): list of demographic variables to extract in a single batch
        state_code (str): US state 2-digit code
        request_url_pre (str): beginning part api request url 
        request_url_post_1 (str): api request middle bit of string
        request_url_post_2 (str): api request middle bit of string
        api_key (str): api key

    Yields:
        result_df (Dataframe): result of extracting one batch from the US census api
        i: the next index for the batch to be extracted
    """
    for i in range(num_processed, num_to_process):
        print("Processing:", str(i+1))
        #sys.stdout.write("\033[F")  # Cursor up one line
        request = create_api_request_str(vars[i], state_code,
                                         request_url_pre, request_url_post_1, request_url_post_2, api_key)
        result_df = api_extract_batch(vars[i], request)

        yield result_df, i


def extract_by_var(vars, state_codes,
                   request_url_pre, request_url_post_1, request_url_post_2, api_key,
                   tmp_folder, tmp_filename_prefix='', reset=False) -> DataFrame:
    """
    Idempotent function to extract demographic variable ('vars') data for each state
    in 'state_code' from the US census api. Keep track of progress and save a temp table 
    in case gets interupted.
    
    Args: 
        vars (List(str)): list of demographic variables to extract in a single batch
        state_codes (List(str)): List of US state 2-digit codes to process
        request_url_pre (str): beginning part api request url 
        request_url_post_1 (str): api request middle bit of string
        request_url_post_2 (str): api request middle bit of string
        api_key (str): api key
        tmp_folder(str): temp folder to store partial extraction
        tmp_filename_prefix(str): temp filename prefix
        reset(Boolean): reset progress keeper?
        

    Returns:
        results (Dataframe): The resulting table of the extraction 
    """
    # US Census API Query Limits: You can include up to 50 variables
    # in a single API query and can make up to 500 queries per IP
    # address per day. More than 500 queries per IP address per day
    # requires that you register for a Census key.
    # -> I have a key, so I guess its unlimited ?!?

    path = tmp_folder + tmp_filename_prefix + '/'
    progress_fp = path + 'progress.cfg'
    
    if reset and os.path.exists(progress_fp):
        os.remove(progress_fp)
    
    progress = Progress(progress_fp,
                        ['states_processed', 'batches_in_state_processed'])
    export_tmp_fp = path + '/us_census_api_extract.parquet.gzip'
    export_tmp_state_fp = path + '/us_census_api_extract_state.parquet.gzip'

    # Split df into batches smaller than 45 (50 - 5) to satisfy API Query limits
    # vars = np.array_split(vars, 450)
    print(len(vars))
    vars = np.array_split(vars, math.ceil(len(vars)/45))
    print(vars)
    # In case the process gets interupted, start processing from last
    # index processed.
    states_processed = progress.get_int('states_processed')
    states_to_process = len(state_codes)
    batches_in_state_processed = progress.get_int('batches_in_state_processed')
    batches_left_in_state_to_process = len(vars)

    print(f"States processed: {states_processed}")
    print(f"States left to process: {states_to_process}")
    print(f"Demo batches in state processed: {batches_in_state_processed}")
    print(
        f"Demo batches in state left to process: {batches_left_in_state_to_process}")

    results_df = pd.DataFrame()

    if not os.path.exists(export_tmp_fp):
        results_df.to_parquet(export_tmp_fp, compression='gzip')

    for states_processed in range(states_processed, states_to_process):
        print(f'State code: {state_codes[states_processed]}')
        tmp_df = pd.DataFrame()
        for result_df, i in api_state_extract(batches_in_state_processed, batches_left_in_state_to_process,
                                              vars, state_codes[states_processed],
                                              request_url_pre, request_url_post_1, request_url_post_2, api_key):

            # save result locally in a temp file, if temp file exists then join result to existing results
            if not os.path.exists(export_tmp_fp):
                result_df.to_parquet(export_tmp_fp, compression='gzip')
            else:
                tmp_df = result_df.join(tmp_df, how='left')
                tmp_df.to_parquet(export_tmp_fp, compression='gzip')

            # record progress
            progress.increment('batches_in_state_processed')

        tmp_df['state_code'] = state_codes[states_processed]

        # save result locally in a temp file, if temp file exists then join result to existing results
        if not os.path.exists(export_tmp_state_fp):
            tmp_df.to_parquet(export_tmp_state_fp, compression='gzip')
        else:
            results_df = results_df.append(tmp_df)
            results_df.to_parquet(export_tmp_state_fp, compression='gzip')

        # update progress: next state, reset batches
        progress.increment('states_processed')
        progress.reset('batches_in_state_processed')

        if tmp_df.empty:
            print("Census variables already processed.")
            tmp_df = pd.read_parquet(export_tmp_fp)

    if results_df.empty:
        print("All states already processed.")
        results_df = pd.read_parquet(export_tmp_state_fp)

    print("Processing Done.")

    return results_df
