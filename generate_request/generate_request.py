
import pandas as pd
import numpy as np

NUM_REQUEST = 20

def random_dates(start, end, n):
    start_u = start.value//10**9
    end_u = end.value//10**9

    return pd.DatetimeIndex((10**9*np.random.randint(start_u, end_u, n, dtype=np.int64)).view('M8[ns]'))

if __name__ == "__main__":

    t_start = pd.to_datetime('2022-11-30')
    t_end = pd.to_datetime('2022-12-01')
    request = random_dates(t_start, t_end, NUM_REQUEST)

    print(pd.DataFrame(request))


