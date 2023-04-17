
import dash
import pandas as pd
from dash.dependencies import Input, Output
from dash import html, Dash, dcc
import dash_bootstrap_components as dbc
from components import scatter_plots


#~~~Data~~~
docs_df = pd.read_csv("data/document_vectors.csv")
authors_df = pd.read_csv("data/author_vectors.csv")

#~~~App~~~

app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
app.title = "Authorship Analysis"

app.layout = html.Div([
    
    html.Div(className="main-div",
             children=[
                 dbc.Container([
                     dbc.Row(
                         [
                             dbc.Col(dcc.Graph(id="av-plot", figure=scatter_plots.author_vector_plot())),
                             dbc.Col(dcc.Graph(id="dv-plot"))
                         ],
                         className="g-0")])
                 ]
             )
    ])


#~~~Callbacks~~~

@dash.callback(Output("dv-plot", "figure"),
               Input("av-plot", "hoverData"))
def update_dv_plot_hover(selected_author):

    if selected_author:
        author_index = selected_author["points"][0]["pointIndex"]
        return scatter_plots.document_vector_plot(author_index)
    else:
        return scatter_plots.document_vector_plot()
        

if __name__ == "__main__":
    app.run(debug=True)

