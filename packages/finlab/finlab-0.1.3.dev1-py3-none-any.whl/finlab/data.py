import requests
import datetime
import pandas as pd
from io import BytesIO
from . import Token

cache = {}
cache_time = {}

def get(dataset, use_cache=True):

    # use cache if possible
    now = datetime.datetime.now()
    if (use_cache and (dataset in cache) and
        (now - cache_time[dataset] < datetime.timedelta(days=1))):
        return cache['dataset']

    # request for auth url
    request_args = {
        'id_token': Token().get(),
        'bucket_name':'finlab_tw_stock_item',
        'blob_name': dataset.replace(':', '#') + '.feather'
    }

    url = 'https://asia-east2-fdata-299302.cloudfunctions.net/auth'
    auth_url = requests.get(url, request_args)

    # download and parse dataframe
    res = requests.get(auth_url.text)
    df = pd.read_feather(BytesIO(res.content))

    # set date as index
    if 'date' in df:
        df.set_index('date', inplace=True)

    # save cache
    if use_cache:
        cache[dataset] = df
        cache_time[dataset] = now

    return df
