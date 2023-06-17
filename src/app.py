
import dash
from dash.dependencies import Input, Output, State
from dash import html, Dash, dcc, dash_table
import dash_bootstrap_components as dbc
import argparse
import pandas as pd

from components import checklist


#~~~App~~~
app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
app.title = "Authorship Analysis"
app.layout = html.Div([
    
    dbc.Row([checklist, dbc.Col(html.Div(id="test-div"))], className="row1"),
    
    ], className="main-div")



#~~~Callbacks~~~

# @dash.callback(Output("av-plot", "figure"),
#                Input("av-plot", "clickData"))
# def update_clicked_av(clicked_author):
#     if clicked_author:
#         return scatter_plots.author_vector_plot(clicked_author)
#     else:
#         return scatter_plots.author_vector_plot()

# @dash.callback(Output("dv-plot", "figure"),
#                Input("av-plot", "clickData"))
# def update_dv_plot(clicked_author:Dict):
#     if clicked_author:
#         author_index = clicked_author["points"][0]["pointIndex"]
#         return scatter_plots.document_vector_plot(author_index)
#     else:
#         return scatter_plots.document_vector_plot()

# @dash.callback(Output("wc-image", "src"),
#                Input("av-plot", "clickData"))   
# def get_wordcloud(clicked_author):
    
#     if clicked_author:
#         author_index = clicked_author["points"][0]["pointIndex"]
#         wc = retrieve_wc_given_author(author_index)
#         return wc
#     else:
#         return Image.open("data/wordclouds/default_tfidf_wc.png")
    
# @dash.callback(Output("wc-header", "children"),
#                Input("av-plot", "clickData"))  
# def update_wc_header(clicked_author):
#     if clicked_author:
#         author_index = clicked_author["points"][0]["pointIndex"]
#         return f"{get_author_id(author_index)}'s TFIDF word cloud"
#     else:
#         return "Corpus TFIDF word cloud"
    
# @dash.callback(Output("table", "data"),
#                Input("av-plot", "clickData"))
# def update_table(clicked_author):
#     if clicked_author:
#         author_index = clicked_author["points"][0]["pointIndex"]
#         return data_table(author_index)
#     else:
#         return default_table()


@app.callback(Output("test-div", "children"),
               [Input("checklist-button", "n_clicks")],
               [State("checklist", "value")])
def update_author_vector_plot(n_clicks, selected_items):
    if n_clicks:
        return selected_items
    
  
    


def main():
    
    args = argparse.ArgumentParser() 
    args.add_argument("-r",
                      "--rerun_dimensionality_reduction",
                      help="Option to re-run the dimensionality reduction algorithms on the database vectors",
                      action="store_false")
    

    

    app.run(debug=True)

        

if __name__ == "__main__":
    main()