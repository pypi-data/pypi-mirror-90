import pyhdfe
import numpy as np
import pandas as pd
import linearmodels.panel as lmp
import linearmodels.iv as lmiv
import statsmodels.api as sm
import time

N = 10_000_000
K = 100

df = pd.DataFrame(
    {
        "id1": np.random.choice(np.arange(1, int(N / K) + 1), size=N),
        "id2": np.random.choice(np.arange(1, K + 1), size=N),
        "x1": np.random.uniform(size=N),
        "x2": np.random.uniform(size=N),
    }
)

df["y"] = (
        3 * df["x1"]
        + 2 * df["x2"]
        + np.sin(df["id1"])
        + np.cos(df["id2"]) ** 2
        + np.random.uniform(size=N)
)

df["id1"] = pd.Categorical(df["id1"])
df["id2"] = pd.Categorical(df["id2"])

# reg y x1 x2
dep = df["y"]
exog = sm.add_constant(df[["x1", "x2"]])


# areg y x1 x2, a(id1)
#absorb = pd.DataFrame(df["id1"])

#start = time.time()
#a = lmiv.AbsorbingLS(dep, exog, absorb=absorb).fit()
#print(a.params)
#end = time.time()
#print(end - start)

# reghdfe y x1 x2, a(id1 id2)
absorb = df[["id1", "id2"]]

start = time.time()
a = lmiv.AbsorbingLS(dep, exog, absorb=absorb).fit()
print(a.params)
end = time.time()
print(end - start)

@profile
def direct():
    algorithm = pyhdfe.create(absorb)
    variables = pd.concat([dep, df[["x1", "x2"]]], 1)
    residualized = algorithm.residualize(variables)
    y = residualized[:, [0]]
    X = residualized[:, 1:]
    ols = sm.OLS(y, X)
    result = ols.fit()
    result.bse
    print(result.params)

direct()