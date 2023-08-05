# Newscraping

[
![PyPI](https://img.shields.io/pypi/v/newscraping)
![PyPI](https://img.shields.io/pypi/l/newscraping)
](https://pypi.org/project/newscraping/)

This package makes webscraping of financial headlines easy. 

## Suported sources:

- reuters.com/finance/markets
- ft.com/markets

## Installation

Newscraping can be installed from PyPI using `pip` or your package manager of choice:

```
pip install newscraping
```

## Usage

### CLI

You can use newscraping as a CLI tool using the `newscraping` command.  
The package will get the latest headline from reuters and print is in the terminal.  
This is mainly for testing purposes. 

### Python script

You can import the newscraping package in your python project using:

```
from newscraping import news
```

And then use it as:

```
df = news(newspaper="reuters", n_articles=-1, early_date="2020-01-01", verbose=0)
```

- With the default parameters (see above), only the last headline from reuters will be returned
- newspaper argument must be in ["reuters", "financial times"]
- n_articles argument is the number of articles to return, starting with the most recent ones
- early_date argument is the publication date of the earliest article to return
- If both n_articles and early_date are provided, the script will stop scraping when the any condition is met
- Pass verbose=1 to print in the progress of websraping (current page and publication date)

### List of available sources

You can get the list of available sources this package is configured for calling:

```
from newscraping import newspapers
available_sources = newspapers()
```
