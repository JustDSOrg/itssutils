import pathlib
import pandas as pd
import matplotlib.pyplot as plt
from itssutils.viz.plot_config import PlotConfig
from ..metrics.names import MetricNames


def metrics_timeseries(met, col,
                       only_include_rows=None,
                       only_include_entries=None,
                       title='',
                       ylabel=None,
                       savename=None,
                       savecsv=None):
    """ Pass in a DF with 'year' as the last index, plots the other top-level
        indices over time for col """
    config = PlotConfig()
    fig, ax = plt.subplots(figsize=(9,6))
    if only_include_rows:
        met = met.loc[only_include_rows]
    else:
        met = met.loc["All_AgencyName"]
    nblevels = met.index.nlevels
    savedata = []
    for name, df in met.groupby(level=list(range(nblevels-1))):
        if only_include_entries and name not in only_include_entries:
            continue
        old_label = name
        tdf = df.loc[name, col].drop(['All_Year'], axis=0)
        if name == 'Hispanic/Latino':
            name = 'Latinx'
        ax.plot(tdf.index, tdf.values, 'o-', label=name, color=config.get_color(old_label))
        tdf.name = name
        savedata.append(tdf)

    metric_names = MetricNames()
    ax.legend(bbox_to_anchor=(1,1))
    ax.set_ylim(bottom=0)
    ax.set_xlabel('Year', fontsize=14)
    ax.set_ylabel(ylabel if ylabel else col, fontsize=14)

    ax.set_title(title, fontsize=16)
    if 'Rate' in col:
        ax.set_yticklabels(['{:.3g}%'.format(y*100) for y in ax.get_yticks()])
    plt.tight_layout()

    if savename:
        plt.savefig(savename, dpi=300)
        plt.close('all')
        if savecsv:
            save_data = pd.concat(savedata, axis=1)
            csv_savename = pathlib.Path(savename)
            save_data.to_csv(str(csv_savename.with_suffix('.csv')))
    else:
        plt.show()


def raw_timeseries(ts, freq, title, ylabel,
                   grouped=False,
                   savename=None,
                   savecsv=None):
    """ Plot a timeseries from raw data """
    config = PlotConfig()
    fig, ax = plt.subplots(figsize=(9,6))
    savedata = []
    if grouped:
        for i, (label, data) in enumerate(ts):
            tdf = data.iloc[:,0].resample(freq).count()
            old_label=label
            if label=='Hispanic/Latino':
                label = 'Latinx'
            tdf.name=label
            savedata.append(tdf)
            data.iloc[:, 0].resample(freq).count().plot(ax=ax, label=label,
                                                        color=config.get_color(old_label),
                                                        linestyle=config.get_linestyle(label),
                                                        marker='o',
                                                        alpha=0.9)
        savedata = pd.DataFrame(savedata)
        ax.legend(bbox_to_anchor=(1,1))

    else:
        savedata = ts.resample(freq).count()
        savedata.plot(ax=ax, marker='o')

    # Formatting
    ax.set_ylim(bottom=0)
    ax.set_xlabel('Date', fontsize=14)

    ax.set_ylabel(ylabel, fontsize=14)
    ax.set_title(title, fontsize=16)

    plt.tight_layout()
    if savename:
        plt.savefig(savename, dpi=300)
        plt.close('all')
        if savecsv:
            csv_savename = pathlib.Path(savename)
            savedata.T.to_csv(str(csv_savename.with_suffix('.csv')))
    else:
        plt.show()
