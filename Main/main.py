import pandas as pd
import osmnx as ox



if __name__ == "__main__":

    Gmpa_KAIST = ox.load_graphml('Final_KAIST.graphml')
    df_request = pd.read_csv('request_data.csv')

    # print(df_request)
    
    
