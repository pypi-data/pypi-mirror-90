
from rki_data import RKI
import pandas as pd

URL = 'dd4580c810204019a7b8eb3e0b329dd6_0.csv'

def test_init():
    r = RKI(file_url=URL)
    assert(isinstance(r.df, pd.DataFrame))
    assert(set(r.df.keys()) == {'Geschlecht',
                                'Altersgruppe',
                                'Altersgruppe2',
                                'NeuGenesen',
                                'AnzahlGenesen',
                                'NeuerTodesfall',
                                'IdLandkreis',
                                'AnzahlFall',
                                'AnzahlTodesfall',
                                'Refdatum',
                                'Bundesland',
                                'IdBundesland',
                                'NeuerFall',
                                'IstErkrankungsbeginn',
                                'Meldedatum',
                                'Datenstand',
                                'Landkreis'})

def test_init_from_web():
    r = RKI()
    assert(isinstance(r.df, pd.DataFrame))
    assert(set(r.df.keys()) == {'Geschlecht',
                                'Altersgruppe',
                                'Altersgruppe2',
                                'NeuGenesen',
                                'AnzahlGenesen',
                                'NeuerTodesfall',
                                'IdLandkreis',
                                'AnzahlFall',
                                'AnzahlTodesfall',
                                'Refdatum',
                                'Bundesland',
                                'IdBundesland',
                                'NeuerFall',
                                'IstErkrankungsbeginn',
                                'Meldedatum',
                                'Datenstand',
                                'Landkreis'})

if __name__ == '__main__':
    test_init()
    test_init_from_web()
