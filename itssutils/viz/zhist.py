import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf
from itssutils.viz.plot_config import PlotConfig

def get_normal_hist(total_counts, bin_size, bounds=(-5,5)):
    """ Get the expected histogram for a normal distribution with a given total
        Returns tuple of (bin_edges, counts)
    """
    perfect_bins = np.arange(bounds[0]-0.5, bounds[1]+5, bin_size)
    perfect = [total_counts*bin_size*(erf(perfect_bins[zz]) - erf(perfect_bins[zz-1])) \
                for zz in range(1, len(perfect_bins))]
    return (perfect_bins, perfect)


def plot_zhist(zscore_df, focus, title='Z-Score Histogram',
                bin_size=0.5, clip=9.99, bound=10):
    """ Plot a single z-score histogram """
    config = PlotConfig()
    fig, ax = plt.subplots(figsize=(6,6))
    hdf = zscore_df.drop('All_AgencyName')
    total = hdf.notnull().sum()
    bins = np.arange(-bound-bin_size, bound+bin_size, bin_size)
    hdf.clip(-clip, clip).hist(ax=ax, bins=bins, alpha=0.8, label=str(focus),
                                color=config.get_color(focus))

    (normal_bins, normal_data) = get_normal_hist(total, bin_size)
    ax.step(normal_bins[1:], normal_data, color='k', linestyle='--', alpha=0.3)
    ax.grid(color='#999999', which='major', linestyle='-', linewidth=1.5, alpha=0.2)
    ax.grid(color='#aaaaaa', which='minor', linestyle='-', linewidth=1, alpha=0.1)
    ax.set_xlabel('Z-Score', fontsize=12)
    ax.set_ylabel('Counts', fontsize=12)
    ax.set_xlim(-bound, bound)
    ax.set_title(title, fontsize=14)
    lgnd = ax.legend(loc='upper left', fontsize=10)
    plt.show()
