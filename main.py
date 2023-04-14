import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from wordcloud import WordCloud
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
app.title = "Authorship Analysis"









if __name__ == "__main__":
    app.run(debug=True)