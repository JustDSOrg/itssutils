import pathlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

from .plot_config import PlotConfig
from ..metrics.names import MetricNames


def format_axes(ax, ind, xname, xax_label=None):
    # Format the axes wtih percent signs
    ax.xaxis.set_major_formatter(ScalarFormatter())
    if 'Rate' in xname:
        ax.set_xticklabels(['{:.3g}%'.format(x*100) for x in ax.get_xticks()])

    metric_names = MetricNames()
    if xax_label:
        ax.set_xlabel(xax_label, fontsize=14)
    else:
        ax.set_xlabel(metric_names.get_description(xname), fontsize=14)
    ax.set_xmargin(0.1)
    ax.set_ymargin(0.1)

    # Create the legend
    # Format tight
    plt.tight_layout(rect=[0.05, 0.03, 0.95, 0.95])


def make_barplot(df, ind, value_col, only_include=None, title=None,
            savename=None, savecsv=False,
            xax_label=None):
    """make a barplot"""
    config = PlotConfig()

    # Get the x and y data, matched on the index
    y_data = df.loc[ind, value_col].astype(float)
    if value_col.endswith('PerPop'):
        y_data = y_data * 1000
    if y_data.isnull().all():
        plt.close('all')
        return
    if only_include:
        y_data = y_data.reindex(reversed(only_include))

    fig, ax = plt.subplots(figsize=(9,6))
    colors = [config.get_color(ind) for ind in y_data.index]

    as_list = y_data.index.tolist()
    idx = as_list.index('Hispanic/Latino')
    as_list[idx] = 'Latinx'
    y_data.index = as_list

    y_data.plot.barh(ax=ax, color=colors, alpha=1, zorder=2)
    max_width = y_data[np.isfinite(y_data)].max()
    if 'Rate' in value_col:
        for (i, p) in zip(y_data.index, ax.patches):
            if np.isfinite(y_data.loc[i]):
                ax.text(p.get_width()+max_width/100, p.get_y()+0.21, '{:0.1f}%'.format(y_data.loc[i] * 100),
                    fontsize=10)
    else:
        for (i, p) in zip(y_data.index, ax.patches):
            try:
                y = int(y_data.loc[i])
            except:
                y = int(0)
            if np.isfinite(y_data.loc[i]):
                ax.text(p.get_width()+max_width/100, p.get_y()+0.21, y)

    if not ax.get_xlim()[1] <= 0 and np.isfinite(ax.get_xlim()[1]):
        ax.set_xlim(0, ax.get_xlim()[1]*1.15)
    format_axes(ax, ind, value_col, xax_label=xax_label)
    if not title:
        title = ind
    ax.set_title(title, fontsize=16)

    # ax.set_axisbelow(True)z

    if savename:
        plt.savefig(savename, dpi=300)
        plt.close('all')
        if savecsv:
            csv_savename = pathlib.Path(savename)
            y_data.to_csv(str(csv_savename.with_suffix('.csv')))
    else:
        plt.show()

    return ax
