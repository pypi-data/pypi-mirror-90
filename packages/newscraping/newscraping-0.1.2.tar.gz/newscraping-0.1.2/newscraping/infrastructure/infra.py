"""This module provides a class for web scraping. 

Classes
-------
DatasetBuilder

"""

import re
from dataclasses import dataclass
from datetime import date

import pandas as pd
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse


@dataclass
class WebScraper:
    """Scrape headlines and publication dates from news websites

    Attributes
    ----------
    newspaper: str
        Name of the newspaper
    n_articles: int
        Number of headlines to scrape. If n_articles = -1, only the date is used to stop the scraping
    early_date: str
        Scrape articles published between execution date and early_date (included). Format must be "YYYY-MM-DD"
    url: str
        Base URL of the website, defined in settings/base.py
    html_articles: list
        HTML tags identifying the articles of a page, defined in settings/base.py
    html_headline: list
        HTML tags identifying the headline, defined in settings/base.py
    html_date: list
        HTML tags identifying the publication date, defined in settings/base.py

    Methods
    -------
    get_headlines
        Scrape headlines and return the data as a DataFrame
    """

    newspaper: str
    n_articles: int
    early_date: str
    url: str
    html_articles: list
    html_headline: list
    html_date: list

    def get_headlines(self, verbose=0) -> pd.DataFrame:
        """Get headlines and date of news articles.

        Parameters
        ----------
        verbose : int, optional
            Pass verbose=1 to print in the progress of websraping (current page and publication date),
            by default 0

        Returns
        -------
        pd.DataFrame
            Headlines and data scraped, with the name of the website.
        """

        if verbose == 1:
            print(f"\nGetting headlines from {self.newspaper}:")

        headlines = {"headline": [], "date": []}
        date_clean = date.today().strftime("%Y-%m-%d")
        page = 1
        n = 0

        while date_clean >= self.early_date:

            if n > self.n_articles and self.n_articles > 0:
                break

            url = self.url.format(page=page)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            try:
                articles = soup.findAll(self.html_articles[0], class_=self.html_articles[1])
            except:
                break

            if len(articles) < 3:
                break

            for article in articles:
                n += 1
                if n > self.n_articles and self.n_articles > 0:
                    break

                try:
                    headline = article.find(
                        self.html_headline[0], class_=self.html_headline[1]
                    ).text
                    date_ = article.find(self.html_date[0], class_=self.html_date[1]).text

                    if verbose == 1:
                        print(f"Current page:{page}, current date: {date_clean}", end="\r")

                    headline_clean = re.sub(r"[()\#/@;<>{}=~|.?]", " ", headline).strip()
                    date_clean = parse(date_).strftime("%Y-%m-%d")

                    if date_clean < self.early_date:
                        break

                    headlines["headline"].append(headline_clean)
                    headlines["date"].append(date_clean)
                except:
                    pass

            page += 1

        df = pd.DataFrame(headlines)
        df["source"] = self.newspaper

        return df
