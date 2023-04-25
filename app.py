
import dash
import pandas as pd
from PIL import Image
from typing import Dict
from dash.dependencies import Input, Output
from dash import html, Dash, dcc
import dash_bootstrap_components as dbc
from components import scatter_plots


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
   # html.Div(className="wc-div",
             #children=[
                 #dbc.Stack([html.Img(src="", style={'height':'21%', 'width':'21%'}, id="wc-image")])
             #])
    ])


                         
                    

#~~~Callbacks~~~

@dash.callback(Output("dv-plot", "figure"),
               Input("av-plot", "clickData"))
def update_dv_plot(clicked_author:Dict):
    if clicked_author:
        author_index = clicked_author["points"][0]["pointIndex"]
        return scatter_plots.document_vector_plot(author_index)
    else:
        return scatter_plots.document_vector_plot()


    
# @dash.callback(Output("dv-plot", "figure"),
#                Input("av-plot", "hoverData"))   
# def get_wordcloud(hovered_author):

#      if hovered_author:
#         author_index = hovered_author["points"][0]["pointIndex"]

        
#         pil_image = Image.open()
    



        

if __name__ == "__main__":
    app.run(debug=True)

