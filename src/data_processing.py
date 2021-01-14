from pathlib import Path

import pandas as pd

from .__init__ import getlog

# TODO Need to find data for world country population per year from 1980 ->

log = getlog(__name__)
p_data = Path(__file__).parents[1] / 'data'

name = 'world_energy'
p_raw = p_data / f'{name}_raw.csv'
p_clean = p_data / f'{name}.csv'

def df_clean():
    """Read cleaned df from /data"""
    return pd.read_csv(p_clean) \
        .assign(year=lambda x: pd.PeriodIndex(x.year, freq='Y')) \
        .merge(right=df_country(), how='right', on='country_code') \
        .set_index('year') \
        [['country', 'energy_type', 'energy']]

def df_country():
    """Read country code conversion df"""
    p = p_data / 'country_conv.csv'
    return pd.read_csv(p)

def convert_raw_data():
    """
    Read raw data from csv and pre-process
    """

    # rename messy categories
    m_replace = {
        'Consumption (quad Btu)': 'total',
        'Coal (quad Btu)': 'coal',
        'Natural gas (quad Btu)' : 'natural_gas',
        'Petroleum and other liquids (quad Btu)': 'petroleum',
        'Nuclear, renewables, and other (quad Btu)': 'all_renewable',
        'Nuclear (quad Btu)': 'nuclear',
        'Renewables and other (quad Btu)': 'renewables'
    }
    
    df = pd.read_csv(p_raw, header=1) \
        .rename(columns={'Unnamed: 1': 'energy_type'}) \
        .assign(
            country_code=lambda x: x.API.str.split('-', expand=True)[2].backfill(),
            energy_type=lambda x: x.energy_type.str.strip().replace(m_replace)) \
        .pipe(lambda df: df[df.API != 'none']) \
        .dropna(subset=['API']) \
        .replace({'--': pd.NA}) \
        .drop(columns=['API']) \
        .melt(id_vars=['energy_type', 'country_code'], var_name='year', value_name='energy') \
        .set_index('year')
    
    # write cleaned df to csv
    df.to_csv(p_clean)
    
    # write separate df for country_code to country conversion
    # df_country = df[df.API.isnull()] \
    #     [['country_code', 'energy_type']] \
    #     .rename(columns=dict(energy_type='country'))
    
    # p = p_data / 'country_conv.csv'
    # df_country.to_csv(p, index=False)
    
    return df
