# (yet another) RKI Scraper

The RKI is the abbreviation for the German Robert Koch Institut. They are the
central science organisation consulting the German government in health issues.

They also track (count) all sick and deceased persons.

This package shall provide sick and deceased person counts for all German States
(Bundesländer) and Counties (Landkreise).

It downloads the current version of the RKI csv file and parses it into a pandas
dataframe. That's about it, but I haven't found anything similar on the web last
summer.

To try it, do the following:

```bash
~$ pip install rki_scraper
~$ python
```

```python
>>> from rki_scraper import RKI
>>> r = RKI()  # wait a while to download and parse a >>100 MB csv file
>>> r.df.head()
```

If you need help, or find a bug just drop a mail!
