import numpy as np
import pandas as pd
from linearmodels.iv import AbsorbingLS, Interaction
n = 50_000
dep = np.random.standard_normal((n, 1))
exog = np.random.standard_normal((n, 2))
cats = pd.DataFrame({i: pd.Categorical(np.random.randint(1000, size=n)) for i in range(2)})
cont = pd.DataFrame({i + 2: np.random.standard_normal(n) for i in range(2)})
absorb = pd.concat([cats, cont], 1)
mod = AbsorbingLS(dep, exog, absorb=absorb)
res = mod.fit()
iaction = Interaction(cat=cats, cont=cont)
absorb = Interaction(cat=cats)  # Other encoding of categoricals
mod = AbsorbingLS(dep, exog, absorb=absorb, interactions=iaction)
mod.fit()
