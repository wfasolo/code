import pandas as pd
import numpy as np
from scipy.stats import poisson


a=poisson.pmf(1/3, 0.37)
print(a)
print(poisson.pmf(1,a))


