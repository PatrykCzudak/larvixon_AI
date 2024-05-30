import dash
from dash import dcc, html, callback, State, Output, Input
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

navigation_panel = html.Div(
    id="nav-panel",
    children=[
        html.H2("Larvixon AI", style={"color": "white", "padding": "20px"}),
        dbc.Accordion(
            [
            dbc.AccordionItem(
                [
                    html.P("Choose settings:"),
                    dcc.Upload(id="vid-file", children=html.Div(["Drag and Drop or ", html.A("Select a File")]),
                        style={"width": "80%", "height": "40px", "lineHeight": "60px", "borderWidth": "1px", "borderStyle": "dashed", "borderRadius": "5px",
                               "textAlign": "center", "margin": "10px"},
                        accept="video/*",
                        multiple=False),
                    dcc.Input(id="confidence-level", placeholder="Confidence Level" ,value="", type="number", style={
                        'width': '80%', 
                        "margin": "10px", 
                        'color': 'black', 
                        'backgroundColor': 'white',
                        'border': '1px solid black',
                        'borderRadius': '5px',
                        "textAlign": "center",
                        }),
                    dcc.Input(id="output-name", placeholder="Output name" ,value="", type="text", style={
                        'width': '80%', 
                        "margin": "10px", 
                        'color': 'black', 
                        'backgroundColor': 'white',
                        'border': '1px solid black',
                        'borderRadius': '5px',
                        "textAlign": "center",
                        }),
                    dmc.Button("Submit", id="submit-btn"),
                ],
                title="AI Settings",
            ),
            dbc.AccordionItem(
                [
                    html.P("Choose settings:"),
                    dbc.Button("Don't click me!", color="danger"),
                ],
                title="Video cut",
            ),
            ],
            style={'width': '80%', 'height': '100vh', "padding": "20px"},
            start_collapsed=True,
        ),
    ],
    style={"width": "100%", 'height': '100vh', "backgroundColor": "#1A1B1E"},
    )

video_panel = html.Div(
    id="video-panel",
    style={"width": "100%", "padding": "20px"},
    children=[dmc.Loader(id="loader", color="red", size="xl", variant="oval", style={"display": "none"})]
)

table_panel = html.Div(
    id="results-table",
    style={"width": "100%", "padding": "20px"},
)

graph_panel = html.Div(
    id="graph-panel",
    style={"width": "100%", "padding": "20px"},
)

content_panel = dmc.Stack([video_panel, table_panel, graph_panel])

store = dcc.Store(id="AI-settings")
stack = layout = html.Div([
    dbc.Row([
        dbc.Col(navigation_panel, width=4),
        dbc.Col(content_panel, width=8)
    ])
], style={"height": "100vh"})

inside = html.Div([stack, store])
layout = dmc.MantineProvider(theme={"colorScheme": "dark"}, 
                             children=[inside])