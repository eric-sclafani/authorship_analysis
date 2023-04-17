
from dash import html, Dash, dcc
import dash_bootstrap_components as dbc
from components import scatter_plots

app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
app.title = "Authorship Analysis"

app.layout = html.Div([
    
    html.Div(className="tabs-div",
             children=[
                 dbc.Container([
                     dbc.Row([dbc.Col(dcc.Graph(id="av-plot", figure=scatter_plots.author_vector_plot())),
                              dbc.Col(dcc.Graph(id="dv-plot",figure=scatter_plots.document_vector_plot())),
                              ])
                     ])
                 ]
             )
    ])





if __name__ == "__main__":
    app.run(debug=True)

