# us_census_api_extract
This package makes it easy to extract US census data by inputting a list of demographic variables and US state codes.  The results are returned as pandas DataFrame.  As it extracts the data it keeps track of the progress and stores the batches in a temp folder.  If the process gets interrupted, you can run it again and it will continue where it left off (ie. it is idempotent). 

## Install

```
pip install us_census_api_extract
```

## Usage 

Go to the [US census page](https://www.census.gov/data/developers/data-sets.html) to get an api key.  In the example below I am using the American 5-year Community Survey (2018) but you could use any api by changing the 'request_url_pre'. 
```
request_url_pre = "https://api.census.gov/data/2018/acs/acs5/subject?get=NAME,"
request_url_post_1 = "&for=tract:*&in=state:"
request_url_post_2 = "&in=county:*&key="
api_key = your-api-key

state_codes = ['48',  # TX
               '36',  # NY
               '06']  # CA

vars = ['S0101_C01_001E', 'S0101_C01_002E', 'S0101_C01_003E',
       'S0101_C01_004E', 'S0101_C01_005E', 'S0101_C01_006E',
       'S0101_C01_007E', 'S0101_C01_008E', 'S0101_C01_009E',
       'S0101_C01_010E', 'S0101_C01_011E', 'S0101_C01_012E']

tmp_path = your-temp-filepath  # this is where the temp files extracted will be stored.

# extract census demographics from US Census API for all census tracts that are in Texas
df_demo = cenx.extract_by_var(vars, state_codes,
                              request_url_pre, request_url_post_1, request_url_post_2, api_key, 
                              tmp_path)
```