from dash import Dash, dcc, html, Input, Output, State
import dash_mantine_components as dmc
import datetime as dt
import osmnx as ox
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.express as px

app = Dash(__name__, title="dash-dbx", update_title=None)
server = app.server

# plt.use('SVG')

app.layout = dmc.MantineProvider(
    withGlobalStyles=True,
    theme={"colorScheme": "dark"},
    children=dmc.NotificationsProvider(
        [html.Div(
                    [
                            # CROSS FILTER
                            dmc.Group(
                                direction="column",
                                position="center",
                                class_name="global-control",
                                children=[
                                    dmc.Title("KAIST E-Scooter Simulator"),
                                    html.Div( children = [
                                            html.Div(children = [html.H4("Map"),dcc.Dropdown(['KAIST'], '', id='drop-map-data', style= {"width" : "300px",'margin-right' : '60px'})]),
                                            html.H1(" "),
                                            html.Div(children = [html.H4("Request"),dcc.Dropdown(['Request_1'], '', id='drop-request-data', style= {"width" : "300px"})]),
                                        ],
                                        style= { "display" : "flex"},
                                    ),

                                    dmc.Chips(
                                        id="Algorithm",
                                        value="FIFO",
                                        direction="row",
                                        align="center",
                                        variant="filled",
                                        color="orange",
                                        data=[
                                            {
                                                "label": "FIFO",
                                                "value": "FIFO",
                                            },
                                            {"label": "CBBA", "value": "CBBA"},
                                            {"label": "ADMM", "value": "ADMM"},
                                        ],
                                    ),
                                ],
                            ),
                            # TOP 2 FIGURES
                            dmc.Grid(
                                gutter="xl",
                                children=[
                                    dmc.Col(
                                        span=6,
                                        children=html.Div(
                                            className="card",
                                            children=[
                                                # html.Label("Select the x axis category: "),
                                                dmc.SegmentedControl(
                                                    id="scatter-x",
                                                    fullWidth=True,
                                                    value="req_vis",
                                                    data=[
                                                        {"label": "Request Visualization", "value": "req_vis"},
                                                        {"label": "Request Detail", "value": "req_dtl"},
                                                        {"label": "Request Status", "value": "req_on"},
                                                    ],
                                                ),
                                                dmc.LoadingOverlay(
                                                    html.Div(id="loading-customize-output", children=[dcc.Graph()]),
                                                ),
                                            ],
                                        ),
                                    ),
                                    dmc.Col(
                                        span=6,
                                        children=html.Div(
                                            className="card",
                                            children=[
                                                dmc.SegmentedControl(
                                                    id="line-y",
                                                    # label="Select the y axis category:",
                                                    fullWidth=True,
                                                    data=[
                                                        {
                                                            "label": "Results",
                                                            "value": "result",
                                                        },
                                                        {
                                                            "label": "Working",
                                                            "value": "working",
                                                        },
                                                        {
                                                            "label": "Rebalancing",
                                                            "value": "rebalancing",
                                                        },
                                                    ],
                                                    value="result",
                                                ),
                                                dmc.LoadingOverlay(
                                                    dcc.Graph(
                                                        id="demographics2",
                                                    ),
                                                ),
                                            ],
                                        ),
                                    ),
                                ],
                            ),
                        ],
                        className="left-tab",
                    ),
            html.Div(id = 'output-data-upload')
                    ]
    )
)

import plotly.graph_objects as go

@app.callback(Output("loading-customize-output", "children"),
            Input('drop-map-data', 'value'),
            State("loading-customize-output", "children"),
              )

def update_output(map_name,figuredata):

    if map_name == "KAIST":
        Gmpa_KAIST = ox.load_graphml('../Main/Final_KAIST.graphml')
        gdf_nodes,gdf_edges = ox.graph_to_gdfs(Gmpa_KAIST)
        fig = go.Figure(data=go.Scattergeo(
            lon=gdf_nodes['x'],
            lat=gdf_nodes['y'],
            mode='markers',
        ))

        for edgeidx in range(len(gdf_edges)):
            linestrings = gdf_edges['geometry'].iloc[edgeidx]
            x, y = linestrings.xy
            lats_data = y
            lons_data = x

            for i in range(len(lats_data) - 1):
                fig.add_trace(go.Scattergeo(lon=[lons_data[i], lons_data[i + 1]], lat=[lats_data[i], lats_data[i + 1]],
                                            mode='lines', line=dict(width=1, color='red'), ))

        fig.update_geos(lataxis_range=[36.3619, 36.3773], lonaxis_range=[127.3537, 127.3708])
        fig.update_layout(showlegend=False)

        return dcc.Graph(id = 'figuremap', figure=fig)

    return figuredata




# @callback(Output("time", "children"), Input("interval", "n_intervals"))
# def refresh_data_at_interval(interval_trigger):
#     """
#     This simple callback demonstrates how to use the Interval component to update data at a regular interval.
#     This particular example updates time every second, however, you can subsitute this data query with any acquisition method your product requires.
#     """
#     return dt.datetime.now().strftime("%M:%S")
#
#
# @callback(
#     Output("user-demo", "children"),
#     Output("user-comp", "children"),
#     Output("user-header", "children"),
#     Output("user-metrics-fig", "figure"),
#     Output("notifications-user", "children"),
#     Input("user-id", "value"),
#     Input("user-fit", "value"),
# )
# def make_userpage(userid, fitness):
#     df_userdemo, df_userfit = dbx_utils.get_user_data(int(userid), fitness)
#     fig_user = figures.generate_userbar(df_userfit, fitness, userid)
#     df_usercomp = dbx_utils.get_user_comp(fitness)
#
#     header = f"Patient {userid}'s fitness data"
#     user_comparison = comp.generate_usercomp(df_usercomp, userid, fitness)
#     blood_pressure = dmc.Text(
#         f"Blood Pressure Level: {df_userdemo['bloodpressure'][0]}"
#     )
#     chorestelor = dmc.Text(f"Cholesterol Level: {df_userdemo['cholesterol'][0]}")
#     patient_info = dmc.Text(
#         f"Patient is a {df_userdemo['age'][0]} old {df_userdemo['sex'][0].lower()}, weights {df_userdemo['weight'][0]} lbs, and is a {df_userdemo['Smoker'][0].lower()}"
#     )
#
#     notification = f"User data loaded. \n\n3 queries executed with number of rows retrieved: {len(df_userdemo) + len(df_userfit) + len(df_usercomp)}"
#     return (
#         [patient_info, chorestelor],
#         [user_comparison, blood_pressure],
#         header,
#         fig_user,
#         comp.notification_user(notification),
#     )
#
#
# @callback(
#     Output("demographics", "figure"),
#     Output("notifications-scatter", "children"),
#     Input("scatter-x", "value"),
#     Input("comparison", "value"),
# )
# def make_scatter(xaxis, comparison):
#     df_scatter = dbx_utils.get_scatter_data(xaxis, comparison)
#     fig_scatter = figures.generate_scatter(df_scatter, xaxis, comparison)
#     notification = f"Scatter data loaded. \n1 query executed with number of rows retrieved: {len(df_scatter)}"
#     return fig_scatter, comp.notification_scatter(notification)
#
#
# @callback(
#     Output("fitness-line", "figure"),
#     Output("notifications-line", "children"),
#     Input("line-y", "value"),
#     Input("comparison", "value"),
# )
# def make_line(yaxis, comparison):
#     df_line = dbx_utils.get_line_data(yaxis, comparison)
#     fig_line = figures.generate_line(df_line, yaxis, comparison)
#     notification = f"Scatter data loaded. \n1 query executed with number of rows retrieved: {len(df_line)}"
#     return fig_line, comp.notification_line(notification)
#
#
# @callback(
#     Output("heat-fig", "figure"),
#     Output("notifications-heatmap", "children"),
#     Input("heat-axes", "value"),
#     Input("heat-fitness", "value"),
#     Input("comparison", "value"),
#     Input("slider-val", "value"),
# )
# def make_heatmap(axes, fitness, comparison, slider):
#     if len(axes) == 2:
#         df_heat = dbx_utils.get_heat_data(axes[0], axes[1], fitness, comparison, slider)
#         fig_heat = figures.generate_heat(df_heat, axes[0], axes[1], fitness, comparison)
#         notification, action = (
#             f"Scatter data loaded. \n1 query executed with number of rows retrieved: {len(df_heat)}",
#             "show",
#         )
#     else:
#         text = "You must select exactly 2 axes for this plot to display!"
#         fig_heat = figures.create_empty(text)
#         notification, action = "", "hide"
#     return fig_heat, comp.notification_heatmap(notification, action)


if __name__ == "__main__":
    app.run_server(debug=True)