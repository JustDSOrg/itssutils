import pandas as pd
import csv
import os
import pathlib

from .consolidator import consolidate_columns
from .decoder import Decoder, DECODE_COLUMNS
from .date_processor import parse_date_cols


def get_preprocessed_filename(filename):
    """Get the name for the preprocessed directory and file"""
    filepath = pathlib.Path(filename)
    base_name = filepath.stem
    new_file_name = '_'.join([base_name, 'preprocessed.pkl'])
    new_dir = pathlib.Path(os.path.dirname(filepath)) / 'preprocessed'
    if not os.path.exists(new_dir):
        new_dir.mkdir()
    new_file_path = new_dir / new_file_name
    return new_file_path


def process_data(raw_data_df):
    """Processes the raw data"""
    print('Parsing dates...')
    df1 = parse_date_cols(raw_data_df)
    print('Dates parsed.')

    print('Consolidating columns...')
    df2 = consolidate_columns(df1)
    print('Columns consolidated.')

    # Decode values to make them more humanly understandable
    decoder = Decoder()
    decode_cols = DECODE_COLUMNS

    df3 = df2.copy()
    print('Decoding columns...')
    for col in decode_cols:
        df3 = decoder.decode_column(df3, col)
    print('Columns decoded. Done processing!')

    return df3


def load_data(year, filename, preprocess=True, save=False, fast=False):
    """Loads and optionally processes and saves data for a given year from
       the given directory"""
    year_data = pathlib.Path(filename)
    new_file_path = get_preprocessed_filename(filename)

    if fast:
        if os.path.exists(new_file_path):
            print(f'Loading previously processed data from {new_file_path}...')
            df = pd.read_pickle(new_file_path)
            print('Data loaded.')
            return df
        else:
            print('Whoops, no previously processed data to load!',
                  '\nGoing to process everything again.')

    print('Reading raw data from ' + str(year_data) + '...')
    # This is the big step, reading the csv
    df = pd.read_csv(year_data,
                     quoting=csv.QUOTE_NONE,
                     encoding='ISO-8859-1',
                     delimiter='~',
                     na_values=['N/A'],
                     low_memory=False,
                     error_bad_lines=True)
    df['Year'] = int(year)

    # Make sure the columns all have the same names
    name_change = {'Agency': 'AgencyName',
                   'WasASearchConducted': 'SearchConducted',
                   'DriversYearOfBirth': 'DriversYearofBirth'}
    df.rename(index=str, columns=name_change, inplace=True)

    # Ensure that DrugsFound in old data gets mapped to VehicleDrugsFound and DriverPassengerDrugsFound in newer data
    to_copy = {'DrugsFound': ['VehicleDrugsFound', 'DriverPassengerDrugsFound'],}
    for col, new_cols in to_copy.items():
        if col in df.columns:
            for new_col in new_cols:
                df[new_col] = df[col]
            df.drop(col, axis=1)

    # Ensure these columns exist in the old data too, though we have to zero them out because we don't know the values
    to_zero = ['VehicleDrugAmount', 'DriverPassengerDrugAmount']
    for zero_col in to_zero:
        if zero_col not in df.columns:
            df[zero_col] = 0

    if not preprocess:
        print('Raw data loaded.')
        return df

    print('Raw data loaded...')
    df3 = process_data(df)

    if save:
        df3.to_pickle(new_file_path)
        print(f'Pickle saved to {new_file_path}. Done!')

    print('Done loading!')

    return df3


def load_multiple_years(year_filename_list, preprocess=True, save=True, fast=True):
    """ Load multiple years of raw data into a single dataframe for processing """
    df_list = []
    for (year, filename) in year_filename_list:
        df = load_data(year, filename,
                       fast=fast,
                       preprocess=preprocess)
        df_list.append(df)
        if save:
            try:
                savepath = get_preprocessed_filename(filename)
                print("Saving to", str(savepath))
                df.to_pickle(savepath)
            except OSError:
                print("Couldn't save - file too big.")

    ret_df = pd.concat(df_list)

    print('Done!')

    return ret_df


def load_demographic_data(demo_path):
    """ Load demographic data collected from the US Census """
    ddf = pd.read_csv(str(demo_path), index_col=0)

    races = ['black', 'asian', 'white',
             'native_american', 'native_hawaiian',
             'other', 'two_or_more_races']

    hisp_cols = [f'hispanic_or_latino_{r}' for r in races]
    nonhisp_cols = [f'not_hispanic_or_latino_{r}' for r in races]

    assert (ddf[hisp_cols].sum(axis=1) == ddf['hispanic']).all()
    assert (ddf[nonhisp_cols].sum(axis=1) == ddf['non_hispanic']).all()

    return ddf