"""Contains the base parameters for the webscraping scripts.

Can be imported as:
>>> import newscraping.settings.base as stg

"""


PARAMS_NEWSPAPER = {
    "reuters": {
        "newspaper": "Reuters",
        "url": "https://www.reuters.com/news/archive/marketsNews?view=page&page={page}&pageSize=10",
        "html_articles": ["div", "story-content"],
        "html_headline": ["h3", "story-title"],
        "html_date": ["span", "timestamp"],
    },
    "financial times": {
        "newspaper": "Financial Times",
        "url": "https://www.ft.com/markets?page={page}",
        "html_articles": ["li", "o-teaser-collection__item o-grid-row"],
        "html_headline": ["a", "js-teaser-heading-link"],
        "html_date": ["time", "o-date o-teaser__timestamp"],
    },
}
