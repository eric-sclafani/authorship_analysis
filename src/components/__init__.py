import dash_bootstrap_components as dbc


from .checklist import feature_checklist, checklist_button


checklist = dbc.Col(
    [feature_checklist(), checklist_button()], 
    className="checklist", 
    )