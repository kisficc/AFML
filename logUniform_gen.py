import matplotlib.pyplot as mpl
import numpy as np
import pandas as pd
from scipy.stats import rv_continuous, kstest

################################################################################
class logUniform_gen(rv_continuous):
    # random numbers log-uniformly distributed between 1 and e
    def _cdf(self, x):
        return np.log(x/self.a)/np.log(self.b/self.a)
def logUniform(a=1, b=np.exp(1)):
    return logUniform_gen(a=a, b=b, name='logUniform')
################################################################################

a = 1E-3
b = 1E3
size = 10000
vals = logUniform(a=a,b=b).rvs(size=size)

print(kstest(
    rvs = np.log(vals), 
    cdf = 'uniform', 
    args = (np.log(a), np.log(b/a)), 
    N = size)
    )
print(pd.Series(vals).describe())

mpl.subplot(121)
pd.Series(np.log(vals)).hist()
mpl.subplot(122)
pd.Series(vals).hist()
mpl.show()
