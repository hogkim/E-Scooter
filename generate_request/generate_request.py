
import pandas as pd
import numpy as np
import random

NUM_REQUEST = 20
NUM_NODE = 244

def random_dates(start, end, n):
    start_u = start.value//10**9
    end_u = end.value//10**9

    return pd.DatetimeIndex((10**9*np.random.randint(start_u, end_u, n, dtype=np.int64)).view('M8[ns]'))

if __name__ == "__main__":
    t_start = pd.to_datetime('2022-12-01')
    t_end = pd.to_datetime('2022-12-02')

    request = random_dates(t_start, t_end, NUM_REQUEST)

    df_request = pd.DataFrame({})
    df_request['Time'] = pd.DataFrame(request.sort_values())
    df_request

    # duration : 몇 분 사용하고 가져다 놓을 건지 ( 회사가 아는지 모르는지 결정 )
    df_request['Duration'] = pd.DataFrame([5 * random.randint(4, 10) for _ in range(NUM_REQUEST)])
    df_request

    # 예1)
    df_request_with_node = df_request.copy()
    df_request_with_node['startnode'] = pd.DataFrame([random.randint(0, NUM_NODE-1) for _ in range(NUM_REQUEST)])
    df_request_with_node['endnode'] = pd.DataFrame([random.randint(0, NUM_NODE-1) for _ in range(NUM_REQUEST)])
    df_request_with_node.to_csv('./request_data.csv')