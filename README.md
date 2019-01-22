# itssutils
### Illinois Traffic Stops Statistical Study Utilities

This package provides a way to calculate metrics for police traffic stops in Illinois. 
Built for use with data provided from the Illinois Traffic Stop Study.

Check out the [Illinois traffic stops website](https://illinoistrafficstops.com/) to learn more.

## Installation
You can install with `pip`:

`pip install itssutils`

## Usage

Download raw data [from this link](https://www.dropbox.com/sh/u2qq21gib0py19k/AAB4_7fKHjDBWZ2V_2mGH3_ca?dl=0) 
(you can download pre-processed metrics files there as well).

Process the raw data using the `RawITSSData` class.

```
from itssutils.itssdata import RawITSSData
raw = RawITSSData()
raw.load_single_year(2017, '2017_ITSS_Data.txt')
```

You can calculate metrics using the `ITSSMetrics` class.

```
from itssutils.itssdata import ITSSMetrics
met = ITSSMetrics(raw)
met.calculate_metics(['AgencyName', 'DriverRace'])
```

## Getting Started

Try opening up the [getting started notebook](notebooks/getting-started-2017.ipynb) 
and working your way through it to see what the package can do. Be sure to note any issues!

Look for more documentationon the [GitHub Pages site](https://justdsorg.github.io/itssutils/). 