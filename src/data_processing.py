from pathlib import Path

import pandas as pd

from .__init__ import getlog

log = getlog(__name__)

def convert_raw_data():
    p = Path(__file__).parents[1] / 'data/world_energy_raw.csv'
    
    df = pd.read_csv(p)
    
    return df
