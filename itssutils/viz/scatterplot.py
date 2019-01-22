import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from textwrap import fill

from itssutils.viz.plot_config import PlotConfig
from ..metrics.names import MetricNames
from ..metrics.zscores import calculate_zscore


def format_scatterplot_axes(ax, logscaling, limits):
    # Set log scaling if selected
    if logscaling:
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlim(0.01, 1)
        ax.set_ylim(0.01, 1)
    else:
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
    if limits:
        ax.set_xlim(limits)
        ax.set_ylim(limits)

    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.ticklabel_format(axis='both', style='plain')
    ax.set_xticklabels(['{:.3g}%'.format(x*100) for x in ax.get_xticks()])
    ax.set_yticklabels(['{:.3g}%'.format(x*100) for x in ax.get_yticks()])
    ax.set_xmargin(0.1)
    ax.set_ymargin(0.1)
    ax.set_aspect('equal')

    # Create the legend
    ax.plot([0,1], [0,1], 'k--', label='equality', alpha=0.5, zorder=3)
    lgnd = ax.legend(loc='upper left', scatterpoints=1, fontsize=10)
    lgnd.legendHandles[1]._sizes = [300]
    lgnd.legendHandles[1].set_alpha(0.9)
    ax.add_artist(lgnd)

    # Format tight
    plt.tight_layout(rect=[0.05, 0.03, 0.95, 0.95])

    pos = ax.get_position()
    ax.set_position([0.02, pos.y0, pos.width, pos.height])


def format_ratioplot_axes(ax, logscaling, limits):
    # Set log scaling if selected
    if logscaling:
        ax.set_xscale('log')
        # ax.set_yscale('log')
        ax.set_xlim(0.001, 1)
        # ax.set_ylim(0.1, 10)
    else:
        ax.set_xlim(-0.05,1.05)
        # ax.set_yscale('log')
    if limits:
        # ax.set_xlim(limits)
        ax.set_ylim(limits)
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.ticklabel_format(axis='both', style='plain')
    ax.set_xticklabels(['{:.3g}%'.format(x*100) for x in ax.get_xticks()])

    ax.set_xmargin(0.1)
    ax.set_ymargin(0.1)
    # ax.set_aspect('equal')

    ax.plot([-0.5,1.5], [0.0,0.0], 'k--', label='equality', alpha=0.5)
    # Create the legend
    lgnd = ax.legend(loc='upper left', scatterpoints=1, fontsize=10)
    lgnd.legendHandles[1]._sizes = [300]
    lgnd.legendHandles[1].set_alpha(0.9)
    ax.add_artist(lgnd)

    plt.tight_layout(rect=[0.05, 0.03, 0.95, 0.95])
    ax.set_position([0.1, 0.1, 0.6, 0.8])
    # Format tight

    yticklabels = []
    for tick in ax.get_yticks():
        if tick == 0:
            yticklabels.append('equal')
        else:
            yticklabels.append('{:.3g}x'.format(abs(tick)+1))
    # print([(x, y) for (x, y) in zip(ax.get_yticks(), yticklabels)])
    yticklabels[0] = yticklabels[0] + ' less'
    yticklabels[-1] = yticklabels[-1] + ' more'
    ax.set_yticklabels(yticklabels)


def hex2rgb(hex):
    h = hex.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))


def make_scatterplot(df, x_index, y_index, value_col, size_col,
                     population_col=None,
                     limits=None,
                     logscaling=False,
                     scale_factor=None,
                     title=None,
                     z_opacity='binary',
                     z_threshold=5,
                     savecsv=False,
                     as_ratio=False,
                     savename=None):
    """make a scatterplot"""
    config = PlotConfig()
    fig, ax = plt.subplots(figsize=(12, 8))

    # Get the x and y data, matched on the index
    full_x_data = df.loc[x_index]
    full_y_data = df.loc[y_index]
    shared_indices = full_x_data.index.intersection(full_y_data.index).drop('All_AgencyName')
    full_index = full_x_data.index.union(full_y_data.index)
    x_data = full_x_data.loc[shared_indices, value_col].astype(float)
    if isinstance(x_index, tuple):
        x_index_name = ' '.join(x_index)
        y_index_name = ' '.join(y_index)
    else:
        x_index_name = x_index
        y_index_name = y_index
    x_data.name = x_index_name + ' ' + x_data.name
    y_data = full_y_data.loc[shared_indices, value_col].astype(float)
    y_data.name = y_index_name + ' ' + y_data.name

    if as_ratio:
        ratio = y_data / x_data
        ratio = ratio.replace([np.inf, -np.inf], np.nan)
        ratio[ratio < 1] = -1 / ratio[ratio < 1] + 2
        ratio = ratio - 1
        # ratio[np.isfinite(ratio)] = ratio[np.isfinite(ratio)].clip(upper=10, lower=-10)
        ratio.name = y_data.name + ' ratio'
        y_data = ratio

    save_data = pd.concat([x_data, y_data], axis=1)
    save_data.index.name = 'Agency'

    try:
        counts = float(size_col)
        scale_factor = 1000.0 if not scale_factor else scale_factor
    except:
        x_counts = full_x_data.loc[shared_indices, size_col].astype(float)
        x_counts.name = x_index_name + ' ' + size_col
        counts = full_y_data.loc[shared_indices, size_col].astype(float)
        counts.name = y_index_name + ' ' + size_col
        scale_factor = df[size_col].max() if not scale_factor else scale_factor

    alphas = None
    if population_col:
        x_pop_data = full_x_data.loc[shared_indices, population_col].astype(float)
        x_pop_data.name = x_index_name + ' ' + population_col
        y_pop_data = full_y_data.loc[shared_indices, population_col].astype(float)
        y_pop_data.name = y_index_name + ' ' + population_col
        full_data = pd.concat([x_pop_data, x_counts, y_pop_data, counts], axis=1)
        old_cols = full_data.columns
        full_data.columns = ['N_1', 'x_1', 'N_2', 'x_2']
        raw_zscores = full_data.apply(lambda x: calculate_zscore(x['N_2'], x['x_2'], x['N_1'], x['x_1']),
                                    axis=1)
        raw_zscores.name = 'Zscore'
        zscores = raw_zscores.abs().fillna(0)
        if z_opacity == 'gradient':
            alphas = zscores.clip(upper=z_threshold).values / (z_threshold + 1) + 0.1
        elif z_opacity == 'filter':
            alphas = zscores.clip(upper=z_threshold).values / z_threshold
            alphas[alphas < 1] = 0
        elif z_opacity == 'binary':
            alphas = zscores.clip(upper=z_threshold).values / z_threshold - 0.1
            alphas[alphas < 0.9] = 0.1
        full_data.columns = old_cols
        save_data = pd.concat([save_data, full_data, raw_zscores], axis=1)


    sizes = 3.0e4 * counts / scale_factor
    N = len(sizes)

    hex_color = config.get_color(y_index)
    rgb = np.array(hex2rgb(hex_color)) / 255.0
    rgbs = np.array([rgb,]*N)
    circle_colors = np.zeros((N, 4))
    circle_colors[:,:3] = rgbs
    if alphas is not None:
        circle_colors[:,3] = alphas
    else:
        circle_colors[:,3] = 0.7

    ax.scatter(x_data, y_data, s=sizes, c=circle_colors, zorder=4,
                label=y_index, edgecolors='face', linewidths=0.2)
    metric_names = MetricNames()
    if as_ratio:
        format_ratioplot_axes(ax, logscaling, limits)
    else:
        format_scatterplot_axes(ax, logscaling, limits)
    x_label = metric_names.get_description(x_index)
    y_label = metric_names.get_description(y_index)
    ax.set_xlabel(' '.join([str(x_label), 'rate']), fontsize=14)
    label_name = 'rate'
    if as_ratio:
        label_name = 'ratio'
    ax.set_ylabel(' '.join([str(y_label), label_name]), fontsize=14)
    if not title:
        title = metric_names.get_description(value_col)
    ax.set_title(title.replace('(', '\n('), fontsize=16)

    max_val = counts.max(skipna=True)
    if pd.isnull(max_val) or not np.isfinite(max_val) or max_val == 0:
        max_val = 1
    basemax = int(np.log10(max_val))
    size_legend = [10**x for x in range(max(basemax-2, 0),basemax+1)]
    tt = [ax.scatter([], [], s=(3.0e4 * x / scale_factor),
            edgecolors='none', alpha=0.9, color=hex_color) for x in size_legend]
    labels = [str(x) for x in size_legend]
    lh = ax.legend(tt, labels, ncol=1, handlelength=2,
        loc='upper right', bbox_to_anchor=(1.3,0.9), borderpad=1.8, scatterpoints=1,
        handletextpad=1.0, title=fill(metric_names.get_description(size_col), 20))
    lh._legend_box.align='right'

    if savename:
        plt.savefig(savename, dpi=200)
        plt.close('all')
    if savecsv:
        csv_savename = pathlib.Path(str(savename.replace('scatterplots', 'zscores')))
        save_data = save_data.reindex(full_index)
        save_data.index.name = 'Agency'
        save_data.to_csv(str(csv_savename.with_suffix('.csv')))
    else:
        plt.show()

    return ax
