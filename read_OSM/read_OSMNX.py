
import osmnx as ox
import networkx as nx
import pandas as pd
import numpy as np


if __name__ == "__main__":
    # KAIST 위치
    kaist = (36.3709, 127.3613)
    # KAIST 근처 도로 모두 read
    G = ox.graph_from_point(kaist, dist=750, network_type="bike")
    fig, ax = ox.plot_graph(G, node_size=10)

    # 세부적으로 KAIST 내부 도로 아닌부분 필터링
    gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
    new_gdf = gdf_nodes
    new_gdf1 = new_gdf[-0.5157593123218502 * new_gdf.x + new_gdf.y < -29.323675157711996]
    G_new = G
    for i in new_gdf1.index:
        try:
            G_new.remove_node(i)
        except:
            pass

    new_gdf2 = new_gdf[-0.6590909090895878 * new_gdf.x + new_gdf.y < -47.579106363468064]
    for i in new_gdf2.index:
        try:
            G_new.remove_node(i)
        except:
            pass

    new_gdf = gdf_nodes[gdf_nodes.x < 127.3564]
    new_gdf = new_gdf[new_gdf.y > 36.37165]
    for i in new_gdf.index:
        try:
            G_new.remove_node(i)
        except:
            pass

    new_gdf = gdf_nodes[gdf_nodes.y > 36.37588]
    for i in new_gdf.index:
        try:
            G_new.remove_node(i)
        except:
            pass

    new_gdf = gdf_nodes
    new_gdf2 = new_gdf[2.297872340464131 * new_gdf.x + new_gdf.y > 329.0468246857673]
    new_gdf2 = new_gdf2[new_gdf2.y > 36.37037]
    for i in new_gdf2.index:
        try:
            G_new.remove_node(i)
        except:
            pass

    new_gdf = gdf_nodes
    new_gdf = new_gdf[new_gdf.y > 36.37266]
    new_gdf = new_gdf[new_gdf.y < 36.37304]
    new_gdf = new_gdf[new_gdf.x > 127.36686]
    new_gdf = new_gdf[new_gdf.x < 127.36720]
    for i in new_gdf.index:
        try:
            G_new.remove_node(i)
        except:
            pass

    G_new.remove_node(10093887420)
    fig, ax = ox.plot_graph(G_new, node_size=10)

    ox.save_graphml(G, './KAIST.graphml')