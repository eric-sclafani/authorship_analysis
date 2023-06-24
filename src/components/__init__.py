from dash import html

from .checklist import make_feature_checklist
from .radiobutton import make_dataset_radio
from .button import configuration_button

config_header = html.H1("Configuration")
checklist_subheader = html.H2("Select high-level features")
feature_checklist = make_feature_checklist()

radio_subheader = html.H2("Select a dataset")
config_radio = make_dataset_radio()

config_button = configuration_button()