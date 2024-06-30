import pandas
from sidecar import Sidecar
import ipywidgets as widgets
import time
from IPython.display import display, HTML

from .column_summary import EDAHubWidgetColumnSummary
from .custom import EDAHubWidgetCustom


class EDAHubWidget:
    def __init__(self, edahub):
        self.edahub = edahub
        tab_contents = ["Summary", "Schema & Stats", "Warnings", "Charts"]

        self.home = widgets.Tab()
        self.update_button = widgets.Button(description="Update")
        self.update_button.on_click(self.update)
        self.summary = EDAHubWidgetSummary()
        self.column_summary = EDAHubWidgetColumnSummary() 
        self.warnings = EDAHubWidgetWarnings()
        self.custom = EDAHubWidgetCustom()

        self.home.children=[
            self.summary.output,
            self.column_summary.output,
            self.warnings.output,
            self.custom.output
        ]
        self.home.titles = tab_contents

        self.sidecar = Sidecar(title=f'EDAHub({self.edahub.name})', anchor='right')
        with self.sidecar:
            display(widgets.VBox([self.update_button, self.home]))

    def update(self, _, components=["Summary", "ColumnSummary", "Charts"]):
        if "Summary" in components:
            self.summary.update(self.edahub)
        if "ColumnSummary" in components:
            self.column_summary.update(self.edahub)
        if "Charts" in components:
            self.custom.update(self.edahub)

    def get_widget_for_export(self):
        self.column_summary.reset_search_box()
        return self.home


class EDAHubWidgetSummary:
    def __init__(self):
        self.status_text = widgets.Output(layout=widgets.Layout(width='100%'))
        self.status_table = widgets.Output(layout=widgets.Layout(width='100%'))
        self.output = widgets.VBox(
            [self.status_text, self.status_table]
        )

    def update(self, edahub):
        with self.status_text:
            text = f"{len(edahub.tables)} tables"
            self.status_text.clear_output()
            display(HTML(f"<p>{text}</p>"))
            
        with self.status_table:
            self.status_table.clear_output()
            display(HTML(edahub.status_table.to_html()))




class EDAHubWidgetWarnings:
    def __init__(self):
        self.output = widgets.Accordion(children=[])
