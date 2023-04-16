
from dash import html, Dash, dcc
import dash_bootstrap_components as dbc
from components import scatter_plots

app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
app.title = "Authorship Analysis"


app.layout = html.Div([
    html.Div(className="main-div",
             children=[
                 html.H1("Authorship Analysis", className="h1"),
                 html.Hr(),
                 html.H4("By: Eric Sclafani", className="h4"),
                 html.Hr()]),
    
    html.Div(className="tabs-div",
             children=[
                 dcc.Graph(figure=scatter_plots.document_vector_plot())])
    ]
                      )





if __name__ == "__main__":
    app.run(debug=True)

