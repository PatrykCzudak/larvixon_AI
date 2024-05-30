import dash
from dash import dcc, html, callback, State, Output, Input
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import base64
import larvixon_ai.nlp_response as nlp
from moviepy.editor import ImageSequenceClip
import tempfile
import os
import flask


def register_callbacks(app):
    
    server = app.server
    @server.route('/video.mp4')
    def serve_video():
        return flask.send_from_directory(os.getcwd(), 'video.mp4')
    
#tworzenie bazy danych ----------------------------------------------------------------------------------------------------------------------------  
    @app.callback(
        Output("AI-settings", "data"),
        [Input("vid-file", "filename"),
        Input("confidence-level", "value"),
        Input("output-name", "value"),
        Input("submit-btn", "n_clicks")],
        [State("AI-settings", "data")],
        prevent_initial_call=True
    )
    def update_data(uploaded_filename, confidence_value, output_name, nclicks, data):
        if data is None:
            data = {}
        if nclicks is not None:  
            if uploaded_filename:
                data["filename"] = uploaded_filename
            if confidence_value:
                data["confidence"] = confidence_value
            if output_name:
                data["output_name"] = output_name
            return data
        
#zmiana stylu po wgraniu pliku ----------------------------------------------------------------------------------------------------------------------------  
    @app.callback(
        Output("vid-file", "style"),
        Input("vid-file", "filename"),
        prevent_initial_call=True
    )
    def change_upload_style(data):
        if data:
            return {
                "width": "80%", "height": "40px", "lineHeight": "60px", "borderWidth": "1px",
                "borderStyle": "dashed", "borderRadius": "5px", "textAlign": "center",
                "margin": "10px", "backgroundColor": "#d1e7dd", "borderColor": "green"
            }
        else:
            return {
                "width": "80%", "height": "40px", "lineHeight": "60px", "borderWidth": "1px",
                "borderStyle": "dashed", "borderRadius": "5px", "textAlign": "center", 
                "margin": "10px"
            }
            
#wyświetlenie filmiku ---------------------------------------------------------------------------------------------------------------------------- 
    @app.callback(
        Output('video-panel', 'children'),
        Output('results-table', 'children'),
        Output('graph-panel', 'children'),
        Input('submit-btn', 'n_clicks'),
        Input('vid-file', 'contents'),
        State('vid-file', 'filename'),
        State('confidence-level', 'value'),
        State('output-name', 'value')
    )
    def update_results(n_clicks, contents, filename, confidence_level, output_name):
        ctx = dash.callback_context
        button_id = None
        
        if ctx.triggered:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]
            
        if button_id != 'submit-btn':
            raise PreventUpdate
        
        
        response = nlp.get_ai_response(vid_path=filename, confidence_lvl=confidence_level, filename=output_name)
        
        #filmik ---
        video_element = html.Video(src="video.mp4", controls=True, style={"width": "100%"})

        #tabeleczka ---
        table_header = [
            html.Thead(html.Tr([html.Th("Parameter"), html.Th("Value")]))
        ]
        table_body = [
            html.Tbody([
                html.Tr([html.Td("Confidence Level"), html.Td(confidence_level)]),
                html.Tr([html.Td("Output Name"), html.Td(output_name)]),
                html.Tr([html.Td("Filename"), html.Td(filename)]),
            ])
        ]
        
        table = dbc.Table(table_header + table_body, bordered=True, striped=True, hover=True)
        
        #graf ---
        result_graph = dcc.Graph(figure=response)
        
        
        return video_element, table, result_graph    
    
    

    