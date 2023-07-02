#!/usr/bin/env python3

from dash import Patch
from dash.dependencies import Input, Output, State
from dash import html, Dash, dcc
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# project imports
import components as comp
from database import queries
from processing import processing


# ~~~ Globals ~~~
PREVIOUS_AUTHOR = []


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

@app.callback(Output("dv-plot", "figure"),
              Output("av-plot", "figure"),
              Input("config-button", "n_clicks"),
              State("feature-checklist", "value"),
              State("dataset-radio", "value"))
def update_scatter_points(_, selected_features, selected_dataset):
    doc_df, author_df = queries.select_features(selected_features, selected_dataset)
    
    global reduced_doc_df, reduced_author_df # really sloppy way of doing this, but saves a ton of extra work. Will return to this.
    reduced_doc_df = processing.apply_dv_pipeline(doc_df)
    reduced_author_df = processing.apply_av_pipeline(author_df)
    
    return comp.document_vector_plot(reduced_doc_df), comp.author_vector_plot(reduced_author_df)
    

@app.callback(Output("dv-plot", "figure", allow_duplicate=True),
              Input("av-plot", "clickData"),
              prevent_initial_call=True)
def update_dv_selected_documents(clicked_author):
    if clicked_author:
        author_index = clicked_author["points"][0]["pointIndex"]
        selected_doc_ids = comp.get_doc_ids_given_author(author_index, reduced_doc_df, reduced_author_df)

        updated_markers = [
            "red" if doc_id in selected_doc_ids else "gray" for doc_id in reduced_doc_df.index 
        ]
        updated_opacity = [
            1 if doc_id in selected_doc_ids else 0.35 for doc_id in reduced_doc_df.index
        ]
        patched_figure = Patch()
        patched_figure["data"][0]["marker"]["color"] = updated_markers
        patched_figure["data"][0]["marker"]["opacity"] = updated_opacity
        return patched_figure
    
@app.callback(Output("av-plot", "figure", allow_duplicate=True),
              Input("av-plot", "clickData"),
              prevent_initial_call=True)
def update_av_clicked_author(clicked_author):
    patched_figure = Patch()
    if clicked_author:
        if PREVIOUS_AUTHOR:
            del patched_figure["data"][0]
            del PREVIOUS_AUTHOR[0]
            
        if not PREVIOUS_AUTHOR:
            x = clicked_author["points"][0]["x"]
            y = clicked_author["points"][0]["y"]
            PREVIOUS_AUTHOR.append((x,y))
            
        author_index = clicked_author["points"][0]["pointIndex"]
        author_id = comp.get_author_id(author_index, reduced_author_df)
        
        patched_figure["data"].insert(
            0,
            go.Scatter(
                x = [x],
                y = [y],
                mode="markers",
                marker_symbol="circle-open",
                marker_size=16,
                text=author_id,
                hoverinfo="skip",
                showlegend=False
)
            )
        return patched_figure

        

def main():
    app.run(debug=True)

    
if __name__ == "__main__":
    main()