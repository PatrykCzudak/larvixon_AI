from dash import Dash
from larvixon_ai.callbacks import register_callbacks
import larvixon_ai.layout as ly
from flask import Flask, send_from_directory
import os

FA = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"
BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css"
XD = "https://unpkg.com/@mantine/dates@7/styles.css"


app = Dash(__name__,
           suppress_callback_exceptions=True,
           external_stylesheets=[FA, BS, XD],
)

app.title ="Larvixon AI"
app.layout = ly.layout

register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, port=8000)