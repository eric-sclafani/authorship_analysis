
import dash
import pandas as pd
from PIL import Image
from dash.dependencies import Input, Output
from dash import html, Dash, dcc
import dash_bootstrap_components as dbc
from components import scatter_plots

#~~~App~~~

pil_image = Image.open('data/wordclouds/en_110_wc.png')
app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
app.title = "Authorship Analysis"

app.layout = html.Div([
    
    html.Div(className="scatter-div",
             children=[
                 
                 dbc.Stack([dcc.Graph(id="av-plot", figure=scatter_plots.author_vector_plot()), dcc.Graph(id="dv-plot")],
                           gap=0,
                           direction="horizontal")]
             ),
    html.Div(className="wc-div",
             children=[
                 dbc.Stack([html.Img(src=pil_image, style={'height':'21%', 'width':'21%'})])
             ])
    ])


                         
                            
# compare each feature
# |value - mean| / std


#~~~Callbacks~~~

@dash.callback(Output("dv-plot", "figure"),
               Input("av-plot", "hoverData"))
def update_dv_plot_hover(hovered_author):

    if hovered_author:
        author_index = hovered_author["points"][0]["pointIndex"]
        return scatter_plots.document_vector_plot(author_index)
    else:
        return scatter_plots.document_vector_plot()
    
    
def get_author_id():
    author_id = "en_110"
    
    image_filename = f'data/wordclouds/{author_id}_wc.svg'
    return image_filename
    # encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode() 
    # return encoded_image

        

if __name__ == "__main__":
    app.run(debug=True)

