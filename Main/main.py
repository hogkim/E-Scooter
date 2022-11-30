import pandas as pd
import osmnx as ox



if __name__ == "__main__":

    Gmpa_KAIST = ox.load_graphml('../read_OSM/KAIST.graphml')
    df_request = pd.read_csv('../generate_request/request_data.csv')

    print(Gmpa_KAIST)
    print(df_request)
