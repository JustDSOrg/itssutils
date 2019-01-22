import pandas as pd
from functools import lru_cache

# Caching each portion of each timestamp so that things run faster
# (20x+, which matters when we're going to do this for every dataset + much more data)


@lru_cache(maxsize=None)
def fast_date_parse(text_datetime):
    """ Caching function for datetime """
    return pd.to_datetime(text_datetime)


@lru_cache(maxsize=None)
def fast_get_time(text_datetime):
    """ Caching function for time """
    return fast_date_parse(text_datetime).time()


@lru_cache(maxsize=None)
def fast_get_timedelta(time):
    """ Caching function for timedelta """
    return pd.to_timedelta(time.isoformat())


def get_date(datetimestring):
    """ Function used to separate date_processor from date when both in same column

        Assume the formatting is 'MM/DD/YYYY HH:MM:SS AM'"""
    return datetimestring.split(' ')[0]


def get_time(datetimestring):
    """ Function used to separate time from date when both in same column

        Some times are improperly formatted. Make sure each hour is modded
        by 24. Default to returning one second after midnight.
        Assume the formatting is 'MM/DD/YYYY HH:MM:SS AM'"""
    sp = datetimestring.split(' ')
    if len(sp) > 1:
        hms = sp[1].split(':')
        hour = hms[0]
        hour = int(hour) % 24
        hour = '{:02d}'.format(hour)
        hms = ':'.join([hour] + hms[1:])
        return hms
    return '00:00:01 AM'


def parse_date_cols(df):
    """ Parse DateAndTimeOfStop into more modern, separate DateOfStop and
        TimeOfStop """
    if 'DateAndTimeOfStop' in df.columns:
        df.loc[:, 'DateOfStop'] = df.DateAndTimeOfStop.apply(get_date)
        df.loc[:, 'TimeOfStop'] = df.DateAndTimeOfStop.apply(get_time)
    df.loc[:, 'DateOfStop'] = df.DateOfStop.apply(fast_date_parse)
    df.loc[:, 'TimeOfStop'] = df.TimeOfStop.apply(fast_get_time)
    stop_timedelta = df.TimeOfStop.apply(fast_get_timedelta)
    df.loc[:, 'StopDateTime'] = df.DateOfStop + stop_timedelta
    return df
