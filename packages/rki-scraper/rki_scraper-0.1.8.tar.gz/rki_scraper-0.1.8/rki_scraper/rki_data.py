
import requests
import os
import pandas as pd
from pathlib import Path
from datetime import datetime
import tempfile

import time

class RKI():
    """Main RKI Class, provides DataFrame."""

    def __init__(self, file_url='https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.csv'):
        """Init RKI Class, default csv given by arcgis."""

        isURL = file_url[:4] == 'http'  # check file_url shorter than 4
        if isURL:
            self.df = self._DF_from_URL(file_url)
        else:
            self.df = self._DF_from_CSV(file_url)


    def _DF_from_CSV(self, csv_path):
        """Load Data from CSV."""
        pandas_arguments = {'index_col': 0,
                            'parse_dates': [8, 10, 13],
                            'date_parser': self._dateparser}

        rki = pd.read_csv(csv_path, **pandas_arguments)

        return rki


    def _DF_from_URL(self, url_str):
        """Load CSV from Internet, save, parse and delete."""
        r = requests.get(url_str, allow_redirects=True)

        fid, temp_file_path = tempfile.mkstemp()
        os.close(fid)
        with open(temp_file_path, 'wb') as fid:
            fid.write(r.content)

        rki = self._DF_from_CSV(temp_file_path)
        os.remove(temp_file_path)

        return rki


    @staticmethod
    def _dateparser(X):
        """Parse RKI CSV date formats (there a two different ones)."""

        try:
            parsed = [datetime.strptime(x, '%d.%m.%Y, %H:%M Uhr') for x in X]
        except ValueError:
            parsed = [datetime.strptime(x, "%Y/%m/%d %H:%M:%S") for x in X]

        return parsed