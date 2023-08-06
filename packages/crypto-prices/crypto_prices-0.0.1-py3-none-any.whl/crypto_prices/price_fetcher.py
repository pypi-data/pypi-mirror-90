import requests
import pandas as pd
from datetime import datetime
from tqdm.auto import tqdm
from multiprocessing.pool import ThreadPool
import time
import logging

SECONDS_MAPPING = {
    'min': 60,
    'H': 60*60,
    'D': 24*60*60
}
BASE_URL = "https://min-api.cryptocompare.com/data/{}"
FREQ_STR = {
    "min": "histominute",
    "H": "histohour",
    "D": "histoday"
}
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
_logger = logging.getLogger(__name__)


def _gen_next_ts(start_ts, freq_str='min', step=2000):
    ts_closest_minute = int(start_ts // 60 * 60)
    delta = step * SECONDS_MAPPING[freq_str]
    end_ts = ts_closest_minute + delta
    return end_ts

def _gen_req_ts_list(from_dt, to_dt=None, freq_str='min', step=2000):
    next_ts = from_dt.replace(second=0, microsecond=0).timestamp()
    if to_dt is None:
        to_dt = datetime.now().replace(second=0, microsecond=0)

    ts_list = []
    while next_ts < to_dt.timestamp():
        next_ts = _gen_next_ts(next_ts, freq_str=freq_str, step=step)
        ts_list.append(next_ts)

    return ts_list

def _single_fetch(args):
    url = args['url']
    retry_count = args['single_call_retry_count']
    delay_between_attempts = args['delay_between_retry_attempts']
    r = requests.get(url, headers=HEADERS)
    resp_json = r.json()
    if resp_json['Response'] != 'Success':
        if retry_count > 0:
            _logger.debug(f"URL: {url} threw error: {resp_json['Message']}, retries left #{retry_count - 1}")
            time.sleep(delay_between_attempts)
            args['single_call_retry_count'] = args['single_call_retry_count'] - 1
            return _single_fetch(args)
        else:
            _logger.error(f"URL: {url} threw error: {resp_json['Message']}")
            return pd.DataFrame()
    df = pd.DataFrame(r.json()['Data'])
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

def fetch_prices(from_sym,
                 to_sym,
                 from_date,
                 to_date=None,
                 freq='H',
                 single_call_retry_count=10,
                 delay_between_retry_attempts=3,
                 n_threads=15):
    """
    :param crypto_symbol: <str> symbol of crypto whose price needs to be fetched e.g. BTC
    :param base_symbol: <str> base currency, e.g. USD
    :param from_dt: <datetime> from what date the prices should be fetched
    :param to_dt: <datetime> to what datetime should the prices be fetched (defaults to now, if None)
    :param freq: <str> One of [min (minutely), H (Hourly), D (Daily)]
    :param single_call_retry_count: <int> If an error occurs, how many times should a call be retried
    :param delay_between_retry_attempts: <int> seconds to wait before retrying
    :param n_threads: <int> number of threads to parallelise the calls
    :return: <pd.DataFrame> Prices data
    """
    ticks_per_call = 2000
    to_ts_list = _gen_req_ts_list(from_dt=from_date,
                                  to_dt=to_date,
                                  freq_str=freq,
                                  step=ticks_per_call)
    freq_url = BASE_URL.format(FREQ_STR[freq])
    urls_list = [f"{freq_url}?toTs={ts}&fsym={from_sym}&tsym={to_sym}&limit={ticks_per_call}" for ts in to_ts_list]
    # Need to pass in the params to_single_fetch method as a single param, for imap call (to allow for progress bar)
    method_args = [
        {'url': url,
         'single_call_retry_count': single_call_retry_count,
         'delay_between_retry_attempts': delay_between_retry_attempts}
        for url in urls_list
    ]
    with ThreadPool(processes=n_threads) as pool:
        responses = list(
            tqdm(pool.imap(_single_fetch, method_args), total=len(method_args))
        )
    return pd.concat(responses)
