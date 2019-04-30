from bokeh.models.widgets import Tabs
from bokeh.io import curdoc
from bokeh.sampledata.us_states import data as states

from scripts.dashboardO3 import o3_tab

# Create tabs
tab1 = o3_tab()

# Put tabs into one application
tabs = Tabs(tabs = [tab1])

# Put the tabs in the current document for display
curdoc().add_root(tabs)