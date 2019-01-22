"""
This module contains two classes: A :class:`RawITSSData` class for reading in raw ITSS
data, processing it, and plotting timeseries of basic counts; and a
:class:`ITSSMetrics` class for computing metrics for various groupings of the raw ITSS
data.

"""

import pandas as pd
import pickle

from .loader.load_raw import load_data, load_multiple_years
from .viz import timeseries, scatterplot, zhist, barplot, ratioplot
from .metrics import metrics, zscores, names


class RawITSSData(object):
    """Human-readable wrappers around raw ITSS data manipulations

    Attributes:
        raw_data_df (pd.DataFrame): raw dataframe
    """

    def load_single_year(self, year, filename, fast=True, save=False):
        """ Load a single year of raw data

        Args:
            year (int): The year of interest
            filename (str): The filename containing raw ITSS data
            fast (bool): Whether to load from pre-processed pickle file
            save (bool): Whether to save to a pickle file

        Returns:
            None

        Example:
            >>> rid.load_single_year(2016, '2016_ITSS_Data.txt')

        """
        self.raw_data_df = load_data(year, filename, fast=fast, save=save)

    def load_multiple_years(self, year_file_list, fast=True, save=False):
        """Load multiple years worth of raw data into a single object

        Args:
            year_file_list (list): List of tuples of the format (year, filename)

        Example:
            >>> yf_list = [(2012, '2012_ITSS_Data.txt'), (2013, '2013_ITSS_Data.txt')]
            >>> rid.load_multiple_years(yf_list)
        """
        self.raw_data_df = load_multiple_years(year_file_list, fast=fast, save=save)

    def get_collected_data(self):
        """Get a list of all the categories of data collected and processed"""
        return self.raw_data_df.dtypes

    def get_agencies(self):
        """Return a list of all reporting agencies"""
        return self.raw_data_df.AgencyName.unique().tolist()

    def get_raw_dataframe(self):
        """Return the underlying dataframe"""
        return self.raw_data_df

    def plot_timeseries(self,
                        frequency='1W',
                        agency=None,
                        filter_cols=None,
                        filter_values=True,
                        group=None,
                        title='All Agencies',
                        savename=None,
                        savecsv=None):
        """Plot a time series of the counts of raw traffic stop data.

        Args:
            frequency (str): the pandas-style sampling frequency; default 1W
            agency (str): The agency to filter by; default None
            filter_cols (str or list): The column(s) to filter by; default None
            filter_values (str or int or list) The selected value(s) to filter by within the filter column
            group (list of str): The column to group by: default None
            title (str): Plot title
            savename (str or path): Path to save figure
            savecsv (str or path): Path to save csv of data used to create figure

        Examples:
            >>> # Find the daily number of stops by the Chicago Police
            >>> rid.plot_timeseries(frequency='1D', agency='Chicago Police')

            >>> # Find the weekly number of citations issued across all departments
            >>> rid.plot_timeseries(filter_cols='ResultOfStop', filter_values='Citation')

            >>> # Find the monthly number of stops by race
            >>> rid.plot_timeseries(frequency='1M', group='DriverRace')
        """
        ts = self.raw_data_df.set_index('StopDateTime')
        ylabel = 'Stop Count'

        grouped = True if group else False

        # Select only a single agency if given
        if agency:
            ts = ts[ts.AgencyName == agency]
            if not title:
                title = agency + ' (' + frequency + ')'

        # Filter all the stops by a given column/value(s) pair
        if filter_cols:
            filter_values = [filter_values] if not isinstance(filter_values, list) else filter_values
            filter_cols = [filter_cols] if not isinstance(filter_values, list) else filter_cols
            for col in filter_cols:
                ts = ts[ts[col].isin(filter_values)]

        # Group by a given category if chosen
        if group:
            group = [group] if not isinstance(group, list) else group
            ts = ts[group].groupby(group)
        else:
            ts = ts.DateOfStop

        timeseries.raw_timeseries(ts, frequency, title, ylabel,
                                  grouped=grouped,
                                  savename=savename,
                                  savecsv=savecsv)


class ITSSMetrics(object):
    """Class to wrap ITSS metrics dataframe

    Attributes:
        raw_df (pd.DataFrame): The dataframe of raw ITSS data
        metrics (pd.DataFrame): The dataframe of calculated metrics
        grouping (list of str): The grouping of calculated metrics
    """

    def __init__(self, itss_data=None):
        """Constructor requires a RawITSSData to initialize, or none if loading
        from a saved csv

        Args:
            itss_data (optional, :class:`RawITSSData`)
        """
        if itss_data:
            self.raw_df = itss_data.raw_data_df
        else:
            self.raw_df = None

        self.grouping = None
        self.metrics = None

    def calculate_metrics(self, grouping, population_csv=None):
        """ Calculate the metrics, grouping by different items

        Args:
            grouping (str or list of str): Columns by which to group the data
            population_csv (str or path): Filename of population demographic csv

        Examples:
            >>> # Calculate the metrics for each racial group across all traffic stops
            >>> mdf = metrics_by_group(raw_data_df, 'DriverRace')

            >>> # Calculate yearly metrics by driver sex for each agency
            >>> mdf = metrics_by_group(raw_data_df, ['AgencyName', 'Year', 'DriverSex'])
        """
        self.metrics = metrics.metrics_by_group(self.raw_df,
                                                grouping,
                                                population_csv=population_csv)
        self.grouping = grouping

    def get_grouping(self):
        """ Return the grouping used to calculate the metrics"""
        return self.grouping

    def get_metrics_df(self):
        """ Return the raw metrics dataframe """
        return self.metrics

    def get_metrics(self):
        """ Return a list of all the calculated metrics """
        name_map = names.MetricNames()
        my_metrics = {met: name_map.get_description(met) for met in self.metrics.columns.tolist()}
        return my_metrics

    def _set_level_last(self, name):
        indices = list(range(len(self.grouping)))
        name_index = self.grouping.index(name)
        indices.append(indices.pop(name_index))
        return self.metrics.reorder_levels(indices).sort_index()

    def plot_scatter(self, y_index, x_index, metric, size,
                     population_col=None,
                     logscale=False,
                     limits=None,
                     scale_factor=None,
                     z_threshold=5,
                     z_opacity='binary',
                     as_ratio=False,
                     title=None,
                     savename=None,
                     savecsv=False):
        """ Scatter plot of all agencies

            Args:
                y_index (str or tuple): the top-level index to use for the y-axis data (i.e. all levels except agency name)
                x_index (str or tuple): the top-level index to use for the x-axis data
                metric (str): the name of the calculated rate to plot, e.g. SearchRate
                size (str): the name of the metric to use to size the points, e.g. SearchCount
                logscale (bool): Plot on a loglog scale
                limits (list or tuple): the limits on the x and y set_axis
                scale_factor (float): Scaling factor for size of points
                z_threshold (float): Cutoff threshold to consider something "statistically significant"
                z_opacity (str): Type of shading to use ('binary', 'gradient', 'filter')
                as_ratio (bool): Make a ratio plot
                title (str): Title of the plot
                savename (str or path): Where to save the figure
                savecsv (str or path): Where to save a csv of data used to make the figure

            Examples:
                >>> # Compare search rates for black and white drivers
                >>> met.plot_scatter('Black', 'White', 'SearchRate', 'SearchCount', population_col='StopCount')
        """
        sdf = self._set_level_last('AgencyName')
        ax = scatterplot.make_scatterplot(sdf, x_index, y_index, metric, size,
                                     population_col=population_col,
                                     logscaling=logscale, limits=limits, scale_factor=scale_factor,
                                     z_threshold=z_threshold, z_opacity=z_opacity, as_ratio=as_ratio,
                                     title=title, savename=savename, savecsv=savecsv)
        return ax

    def plot_zhist(self, target_item, reference_item, event_col, total_obs_col, title=None):
        """ Z-score histogram for a given event/observation count pairing,
            e.g. SearchCount/StopCount
            Must have included 'AgencyName' in grouping and grouping must be
            at least two categories

            Args:
                target_item: index of target item, e.g. 'Black'
                reference_item: index of reference item, e.g. 'White'
                event_col: column name for event counts, e.g. SearchCount
                total_obs_col: column name for total observations, e.g. StopCount

            Examples:
                >>> # Compare the deviation of black driver search hit rate relative to white driver search hit rate
                >>> met.plot_zhist('Black', 'White', 'SearchHitCount', 'SearchCount')
        """
        assert 'AgencyName' in self.grouping and len(self.grouping) > 1
        sdf = self._set_level_last('AgencyName')
        zdf = zscores.get_zscore_df(sdf, target_item, reference_item,
                                    event_col, total_obs_col)
        if not title:
            title = (event_col, total_obs_col)
        zhist.plot_zhist(zdf, target_item, title=title)
        return zdf

    def plot_bars(self, target_top_row, target_column,
                  only_include_rows=None,
                  title=None,
                  savename=None,
                  savecsv=False,
                  xax_label=None):
        """ Make a bar plot of a certain metric.
            Requires a multi-level metrics calculation be passed in.

            Args:
                target_top_row (str):

            Examples:
                >>> met.calculate_metrics(['AgencyName', 'DriverRace'])
                >>> met.plot_bars('Chicago Police', 'SearchRate')

        """
        barplot.make_barplot(self.metrics, target_top_row, target_column,
                             only_include=only_include_rows,
                             title=title,
                             savename=savename,
                             savecsv=savecsv,
                             xax_label=xax_label)

    def plot_timeseries(self, target_column,
                        only_include_rows=None,
                        only_include_entries=None,
                        title=None,
                        ylabel=None,
                        savename=None,
                        savecsv=None):
        """ Make a timeseries plot

        Args:
            target_column (str): The column you want to make the timeseries for
            only_include_rows (str or tuple or list): Rows of index to include
            only_include_entries (str or tuple or list): Filter criteria - only include matching entries from target
            title (str): Plot title
            ylabel (str): Plot y-axis label
            savename (str or path): Path to save the plot
            savecsv (str or path): Path to save a csv of data used to make the plot

        Examples:
            >>> met.plot_timeseries('SearchRate', only_include_rows='Chicago Police', only_include_entries=['Black', 'Hispanic/Latino', 'Asian', 'White'], title='Search Rate 2012-2017')
        """
        sdf = self._set_level_last('Year')
        timeseries.metrics_timeseries(sdf, target_column,
                                      only_include_rows=only_include_rows,
                                      only_include_entries=only_include_entries,
                                      title=title, ylabel=ylabel,
                                      savename=savename,
                                      savecsv=savecsv)

    def load(self, filename):
        """ Load a metrics object from a pickle file
            pickled object is (grouping, metrics_df) tuple
         """
        self.grouping = None
        self.metrics = None
        with open(filename, 'rb') as f:
            (self.grouping, self.metrics) = pickle.load(f)

    def save(self, filename):
        """ Pickle a metrics object as a (grouping, metrics_df) tuple """
        with open(filename, 'wb') as f:
            pickle.dump((self.grouping, self.metrics), f)

    def save_csv(self, filename):
        """ Save the current metrics as a csv file """
        self.metrics.to_csv(filename)
