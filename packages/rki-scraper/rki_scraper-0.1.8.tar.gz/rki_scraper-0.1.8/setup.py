from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'rki_scraper', 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='rki_scraper',
      version='0.1.8',
      description='Scrape the RKI Data from Arcgis into a Pandas Dataframe',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['rki_scraper'],
      include_package_data=True,
      author='Grzegorz Lippe',
      install_requires=['pandas',
                        'requests'],
      author_email = 'grzegorz.lippe@posteo.de',
      zip_safe=False)
