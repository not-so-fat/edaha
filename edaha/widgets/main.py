import pandas
from sidecar import Sidecar
import ipywidgets as widgets
import time
from IPython.display import display, HTML

from .column_summary import EDAHAWidgetColumnSummary


class EDAHAWidget:
    def __init__(self, edaha):
        self.edaha = edaha
        tab_contents = ["Summary", "Schema & Stats", "Warnings"]
        self.sidecar = Sidecar(title=f'EDAHA({self.edaha.name})', anchor='right')
        self.update_button = widgets.Button(description="Update")
        self.update_button.on_click(self.update)
        self.summary = EDAHAWidgetSummary()
        self.column_summary = EDAHAWidgetColumnSummary() 
        self.warnings = EDAHAWidgetWarnings()
        with self.sidecar:
            tab = widgets.Tab()
            tab.children=[
                self.summary.output,
                self.column_summary.output,
                self.warnings.output
            ]
            tab.titles = tab_contents
            display(widgets.VBox([self.update_button, tab]))

    def update(self, _):
        self.summary.update(self.edaha)
        self.column_summary.update(self.edaha)


class EDAHAWidgetSummary:
    def __init__(self):
        self.status_text = widgets.Output(layout=widgets.Layout(width='100%'))
        self.status_table = widgets.Output(layout=widgets.Layout(width='100%'))
        self.output = widgets.VBox(
            [self.status_text, self.status_table]
        )

    def update(self, edaha):
        with self.status_text:
            text = f"{len(edaha.tables)} tables"
            self.status_text.clear_output()
            display(HTML(f"<p>{text}</p>"))
            
        with self.status_table:
            self.status_table.clear_output()
            display(HTML(edaha.status_table.to_html()))




class EDAHAWidgetWarnings:
    def __init__(self):
        self.output = widgets.Accordion(children=[])
