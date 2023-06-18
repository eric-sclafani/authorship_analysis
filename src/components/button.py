
import dash_bootstrap_components as dbc


def configuration_button() -> dbc.Button:
    return dbc.Button(
        "Submit",
        id="config-button",
        className="config-button",
    )
    