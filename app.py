
import dash
from typing import Dict
from dash.dependencies import Input, Output
from dash import html, Dash, dcc
import dash_bootstrap_components as dbc

# project imports
from components import scatter_plots
from components.get_wordcloud import retrieve_wc_given_author, Image
from components.processing import get_author_id
from components.feature_selector import author_identifying_features_pcp, default_pcp_plot


#~~~App~~~
app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
app.title = "Authorship Analysis"

app.layout = html.Div([
    
    html.P(id="dummy"),
    html.Div(className="scatter-div",
             children=[
                 
                 dbc.Stack([dcc.Graph(id="av-plot", 
                                      figure=scatter_plots.author_vector_plot(), 
                                      config={"displayModeBar": False},
                                      ), 
                            
                            dcc.Graph(id="dv-plot", 
                                      config={"displayModeBar": False}
                                      )
                            ],
                           gap=0,
                           direction="horizontal")]
             ),
   html.Div(className="wc-div",
             children=[
                 dbc.Stack([html.Img(style={"height":"23%", "width":"23%"}, id="wc-image"),
                            dcc.Graph(id="pcp")],
                           gap=0,
                           direction="horizontal"),
                 

             ])
    ])


#~~~Callbacks~~~

@dash.callback(Output("dv-plot", "figure"),
               Input("av-plot", "clickData"))
def get_av_clicked_data(clicked_author:Dict):
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
    
    
# @dash.callback(Output("wc-header", "children"),
#                Input("av-plot", "clickData"))  
# def update_wc_header(clicked_author):
#     if clicked_author:
#         author_index = clicked_author["points"][0]["pointIndex"]
#         return f"{get_author_id(author_index)}'s TFIDF word cloud"
#     else:
#         return "Corpus TFIDF word cloud"
    
@dash.callback(Output("pcp", "figure"),
               Input("av-plot", "clickData"))
def update_pcp(clicked_author):
    if clicked_author:
        author_index = clicked_author["points"][0]["pointIndex"]
        return author_identifying_features_pcp(author_index)
    else:
        return default_pcp_plot()
    


        

if __name__ == "__main__":
    app.run(debug=True)

