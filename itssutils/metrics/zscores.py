import pandas as pd
import numpy as np
import statsmodels.api as sm
from tqdm import tqdm

def calculate_zscore(N_1, x_1, N_2, x_2):
    """ Calculate a z-score for a difference between rates """
    xs = np.array([x_1, x_2])
    Ns = np.array([N_1, N_2])
    if any(np.isnan(xs + Ns)) or any (xs > Ns):
        return np.NaN
    elif any(xs < 5) or any(Ns-xs < 5):
        return np.NaN
    z, p = sm.stats.proportions_ztest(xs, Ns)
    if not np.isfinite(z):
        return np.NaN
    return z

def safe_divide(num, den):
    try:
        return num / den
    except ZeroDivisionError:
        return np.NaN

def get_rate_df_for(df, focus, num_col, den_col):
    rdf = df.loc[focus].loc[:, [num_col, den_col]]
    rdf['Rate'] = safe_divide(rdf[num_col], rdf[den_col])
    rdf.columns = ['_'.join([col, str(focus)]) for col in rdf.columns]
    return rdf

def get_zscore_df(df, target, reference, x_col, N_col,
                        newcol_suffix='Z'):
    """ Calculate the z-score of the differences between a given rate
        rate and the reference rate for a rate of interest, e.g. search frequency
        between races or citation frequency between genders

        Uses the index along the first dimension as the reference group, e.g.
        for a dataframe indexed as |Race|Agency|Sex| will use race as the column
        along which to look for the reference"""
    if reference not in df.index or target not in df.index:
        raise KeyError('Reference ' + reference + ' or target ' + target + ' not in index.')
    tgt_df = get_rate_df_for(df, target, x_col, N_col)
    ref_df = get_rate_df_for(df, reference, x_col, N_col)
    min_names = tgt_df.columns
    ref_names = ref_df.columns
    shared_index = tgt_df.index.intersection(ref_df.index)
    tgt_df = tgt_df.loc[shared_index]
    rdf = ref_df.loc[shared_index]
    tdf = pd.concat([tgt_df, ref_df], axis=1, sort=False)
    zscores = tdf.apply(lambda x: calculate_zscore(x[min_names[1]], x[min_names[0]], \
                                                    x[ref_names[1]], x[ref_names[0]]),
                                                    axis=1)
    zscores.name = '_'.join([x_col, N_col, newcol_suffix])

    return zscores
