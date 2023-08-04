import openmc
import pandas as pd
from openmc import deplete

from utils.material import water_mat, fuel_mat

results = openmc.deplete.Results("./depletion_results.h5")
# rates = pd.DataFrame(results[0].rates[0][0])
# print(results[0])
# rates.to_csv('rates.csv')
cols = ['U235', 'U238']
rows = ('(n,2n)', '(n,3n)', '(n,4n)', '(n,a)', '(n,gamma)', '(n,p)', 'fission')
res = []
for rx in rows:
    time, rate_u235 = results.get_reaction_rate(mat=fuel_mat, nuc='U235', rx=rx)
    time, rate_u238 = results.get_reaction_rate(mat=fuel_mat, nuc='U238', rx=rx)
    res.append([rate_u235[0], rate_u238[0]])
df = pd.DataFrame(res, columns=cols, index=rows)
print(df)
df.to_csv("rates_df.csv")
