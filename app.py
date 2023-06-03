
import dash
from typing import Dict
import pandas as pd
from dash.dependencies import Input, Output
from dash import html, Dash, dcc, dash_table
import dash_bootstrap_components as dbc

# project imports
from components import scatter_plots
from components.get_wordcloud import retrieve_wc_given_author, Image
from components.processing import get_author_id
from components.feature_selector import author_identifying_features_pcp, default_pcp
from components.table import data_table, default_table

#~~~Globals~~~
DISPLAY_CFG = {"displayModeBar": False}

#~~~App~~~
app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
app.title = "Authorship Analysis"
app.layout = html.Div([
    
        dbc.Row([
            dbc.Col([dcc.Graph(id="av-plot", config=DISPLAY_CFG)], width=4),
            dbc.Col([dcc.Graph(id="dv-plot", config=DISPLAY_CFG)])]),
             
        dbc.Row([
            dbc.Col([html.H4(id="wc-header"),
                     html.Img(style={"height":"50%", "width":"54%", 'margin': '0px 0px 10px 0px'}, id="wc-image"),
                     dash_table.DataTable(id="table", 
                                          fill_width=False,
                                          style_header={'backgroundColor':'#305D91',
                                                        'padding':'10px',
                                                        'color':'#FFFFFF'},
                                          style_cell={'textAlign':'center',
                                                      'width': 105,
                                                      'font_size': '12px',
                                                      'whiteSpace':'normal',
                                                      'height':'auto'},
                                          )], 
                    style={'padding': '0px 0px 50px 0px'}),
            
            dbc.Col(dcc.Graph(id="pcp", config=DISPLAY_CFG), width=7)], 
                style={'padding': '0px 0px 20px 20px'}, align="center",
                )
                 ]
             )



#~~~Callbacks~~~

@dash.callback(Output("av-plot", "figure"),
               Input("av-plot", "clickData"))
def update_clicked_av(clicked_author):
    if clicked_author:
        return scatter_plots.author_vector_plot(clicked_author)
    else:
        return scatter_plots.author_vector_plot()

@dash.callback(Output("dv-plot", "figure"),
               Input("av-plot", "clickData"))
def update_dv_plot(clicked_author:Dict):
    if clicked_author:
        author_index = clicked_author["points"][0]["pointIndex"]
        return scatter_plots.document_vector_plot(author_index)
    else:
        return scatter_plots.document_vector_plot()


@dash.callback(Output("wc-image", "src"),
               Input("av-plot", "clickData"))   
def get_wordcloud(clicked_author):
    
    if clicked_author:
        author_index = clicked_author["points"][0]["pointIndex"]
        wc = retrieve_wc_given_author(author_index)
        return wc
    else:
        return Image.open("data/wordclouds/default_tfidf_wc.png")
    
@dash.callback(Output("wc-header", "children"),
               Input("av-plot", "clickData"))  
def update_wc_header(clicked_author):
    if clicked_author:
        author_index = clicked_author["points"][0]["pointIndex"]
        return f"{get_author_id(author_index)}'s TFIDF word cloud"
    else:
        return "Corpus TFIDF word cloud"
    
@dash.callback(Output("pcp", "figure"),
               Input("av-plot", "clickData"))
def update_pcp(clicked_author):
    if clicked_author:
        author_index = clicked_author["points"][0]["pointIndex"]
        return author_identifying_features_pcp(author_index)
    else:
        return default_pcp()
    
@dash.callback(Output("table", "data"),
               Input("av-plot", "clickData"))
def update_table(clicked_author):
    if clicked_author:
        author_index = clicked_author["points"][0]["pointIndex"]
        return data_table(author_index)
    else:
        return default_table()
    
  
    
    

    


        

if __name__ == "__main__":
    app.run(debug=True)

