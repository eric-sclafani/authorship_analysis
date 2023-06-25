#!/usr/bin/env python3

import dash
from dash.dependencies import Input, Output, State
from dash import html, Dash, dcc
import dash_bootstrap_components as dbc

# project imports
import components as comp
from database import queries
from processing import processing


#~~~App~~~
app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
app.title = "Authorship Analysis"
app.layout = html.Div([
    html.H1(["Header"], className="header"),
    html.Div([
        html.Div([
            html.H1("Configuration"),
            html.H2("Select high-level features"),
            comp.make_feature_checklist(),
            html.H2("Select a dataset"),
            comp.make_dataset_radio(),
            comp.configuration_button()
            ], className="config"),
        
        html.Div([
            dcc.Graph(id="av-plot", className="av-plot"),
            dcc.Graph(id="dv-plot", className="dv-plot")
            ], className="scatter-plots"),
        
        ], className="middle"),
    ], className="main-div")



#~~~Callbacks~~~

@app.callback(Output("av-plot", "figure"),
              Output("dv-plot", "figure"),
              Input("config-button", "n_clicks"),
              State("feature-checklist", "value"),
              State("dataset-radio", "value"))
def update_author_vector_plot(_, selected_features, selected_dataset):
    
    doc_df, author_df = queries.select_features(selected_features, selected_dataset)
    reduced_doc_df = processing.apply_dv_pipeline(doc_df)
    reduced_author_df = processing.apply_av_pipeline(author_df)
    return comp.document_vector_plot(reduced_doc_df), comp.author_vector_plot(reduced_author_df)
    
  
    


def main():
    app.run(debug=True)

    
if __name__ == "__main__":
    main()