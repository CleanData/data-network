# Data-Network


An app for the visualisation of connections between datasets, part of the Clean Data initiative that began at the [Data Jam at New York Energy Week, 2013](http://energy.gov/articles/putting-data-work-new-york-energy-week).

## Background

Open Data is only useful if you can find it, parse it, and build on it. In many cases it is hard to find data sets - and when they are identified, they are in arcane data formats, or missing key information. Data standards are one approach to solving this problem. Another is to accept that the problem has already been solved many times over by a multitide of researchers.

This tool is designed to highlight the connections between datasets. If you are looking for a dataset, you should be able to see:

* which source datasets feed into the dataset
* which datasets derive from the dataset
* what processing was performed to relate one dataset to another
* who manages the dataset
* who contributes to the dataset
* what license applies to the dataset

Other (extra credit) information that can come out a structured map of relations between datasets are:

* what other datasets are most often used with this dataset (zipcode energy data is often used with zipcode shapefiles, for example)
* issues associated with a dataset - flagged automatically, or by users (10 lies in this file are NaN for example)
* all of the datasets/APIs/web apps/companies that have derived from the dataset (valuable for companies and the government when justifying Open Data initiatives)
* Missing datasets - identify high value datasets that aren't open, yet

By creating a visual network of data we will:

* speed discovery of data sets
* open up access to open data
* enable data scientists to shine
* incentivise collaboration

## Stack

* Python - http://python.org/
* Django - https://www.djangoproject.com
* D3 - http://d3js.org/

