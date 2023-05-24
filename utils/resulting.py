import pandas as pd
import openmc

with openmc.StatePoint('statepoint.100.h5') as sp:
    print(sp)
    output_tally = sp.get_tally()
    df = output_tally.get_pandas_dataframe()
    df.to_csv('out.txt')
    print(df)