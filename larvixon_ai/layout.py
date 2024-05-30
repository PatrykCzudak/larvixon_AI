import dash
from dash import dcc, html, callback, State, Output, Input
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

navigation_panel = html.Div(
    children=[
        html.H2("Larvixon AI", style={"color": "white", "padding": "20px"}),
        dbc.Accordion(
            [
            dbc.AccordionItem(
                [
                    html.P("Choose settings:"),
                    dcc.Upload(id="vid-file", children=[
                        "Select file.",
                        html.A("Choose file")]),
                    dbc.Button("Button"),
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
    style={'width': '30%', 'height': '100vh', "backgroundColor": "#1A1B1E"},
    )

content_panel = html.Div(
    id="page-content",
    style={"marginLeft": "320px",
           "marginRight": "40%",},
)

inside = html.Div([content_panel, navigation_panel])
layout = dmc.MantineProvider(forceColorScheme="dark", 
                             theme={"colorScheme": "dark"}, 
                             children=[inside])