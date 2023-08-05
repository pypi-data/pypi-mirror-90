"""This module provides functions for web scraping. 

Functions
-------
news
newspapers

"""

import pandas as pd

import newscraping.settings.base as stg
from newscraping.infrastructure.infra import WebScraper


def news(
    *,
    newspaper: str = "reuters",
    n_articles: int = -1,
    early_date: str = "2020-01-01",
    verbose: int = 0,
) -> pd.DataFrame:
    """
    Scrape a user-specified number of headlines from a newspaper website,
    starting with the most recent ones.

    Using the default parameters, the function will return a dataframe
    containing the latest headline from reuters.

    Parameters
    ----------
    newspaper : str, optional
        Name of the newspaper to scrape headlines from. Ex: "reuters"
    n_articles : int, optional
        Number of headlines to scrape. Ex: 5
    early_date : str, optional
        Start of the period to scrape headlines from. Ex: "2020-12-25"
    verbose : int, optional
        Pass verbose=1 to print in the progress of websraping (current page and publication date),
        by default 0

    Returns
    -------
    DataFrame
        Headlines with dates and newspaper name

    Raises
    -------
    KeyError
        If the newspaper is not known by the programm
    """

    try:
        params = stg.PARAMS_NEWSPAPER[newspaper]
    except KeyError:
        raise KeyError(f"The newspaper {newspaper} is not available.")

    if n_articles == -1 and early_date == "2020-01-01":
        n_articles = 1

    params["n_articles"] = n_articles
    params["early_date"] = early_date

    return WebScraper(**params).get_headlines(verbose=verbose)


def newspapers():
    return [key for key in stg.PARAMS_NEWSPAPER.keys()]


if __name__ == "__main__":
    df = news()
    print(df.head())
