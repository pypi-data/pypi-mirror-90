import numpy as np
import pandas as pd
from histmp._exp import peek_2d

x = np.array([[1,2,3,4],
              [5,6,7,8],
              [4,3,2,1],
              [8,7,6,5],
              [6,7,8,5],
              [3,1,2,4],
              [4,2,3,1]]).astype(np.float64)
x = pd.DataFrame(x, columns="a b c d".split())

print(x)
print("--")

peek_2d(x.a, x, 5, 7, 8)
