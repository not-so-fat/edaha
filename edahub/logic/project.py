from datetime import datetime
import threading

import pandas
import ipywidgets
from ipywidgets import embed

from ..widgets import EDAHubWidget
from . import stats_calculator
from .vis import histogram


STATUS_COLUMNS = ["name", "#rows", "#cols", "status", "created"]


class EDAHub:
    """
    EDA with a widget at the side bar on JupyterLab
    """
    def __init__(self, name=None):
        self.name = name or _get_name()
        self.tables = {}
        self.status_table = pandas.DataFrame(columns=STATUS_COLUMNS)
        self.stats_tables = {}
        self.histograms = {}
        self.eda_thread = None
        self.custom_objs = {}
        self.widget = EDAHubWidget(self)

    def add_table(self, name, df, overwrite=False):
        """
        Initiate EDA for a pandas.DataFrame and add the result into the widget
        Args:
            name (str): name of data
            df (pandas.DataFrame): data you want to perform EDA to get summary
        """
        if not overwrite and name in self.tables:
            raise Exception(f"name={name} has been already registered. Use a different name or the option `overwrite=True`")
        now = datetime.now().replace(microsecond=0)
        new_row = pandas.DataFrame(
            {k: [v] for k, v in zip(
                STATUS_COLUMNS, [name, len(df), len(df.columns), "computing stats", now]
            )}
        )
        if len(self.status_table):
            self.status_table = pandas.concat([self.status_table, new_row], ignore_index=True)
        else:
            self.status_table = new_row
        self.tables[name] = df
        self.stats_tables[name] = self._get_schema(df)
        self.widget.update(None, ["Summary", "ColumnSummary"])
        self._compute_stats(name, df)
        self._add_histograms(name, df)

    def get_table_names(self):
        """
        Returns:
            list[str] all the names of data registered
        """
        #TODO: sort table names based on created
        return list(self.tables.keys())

    def get_column_names(self, table_name):
        return self.stats_tables[table_name]["column_name"].to_list()

    def add_chart(self, group_name, chart):
        """
        Add a chart into the widget on the tab named "Charts"
        Args:
            group_name (str): Identifier of group in Accordion widget in "Charts" tab
            chart: Object you want to put on the widget, displayed by `display(chart)`
        """
        if group_name not in self.custom_objs:
            self.custom_objs[group_name] = []
        self.custom_objs[group_name].append(chart)
        self.widget.update(None, ["Charts"])

    def export_html(self, filepath):
        widget_for_export = self.widget.get_widget_for_export()
        embed.embed_minimal_html(filepath, widget_for_export, title=f'EDAHub({self.name})')

    def _get_schema(self, df):
        return pandas.DataFrame({
            "column_name": df.columns,
            "dtype": df.dtypes
        })

    def _compute_stats(self, name, df):
        def target():
            self.stats_tables[name] = stats_calculator.calc_column_stat(df)
            self._update_status(name, "generating histograms")
            self.widget.update(None, ["ColumnSummary"])
        
        self.eda_thread = threading.Thread(target=target)
        self.eda_thread.start()

    def _add_histograms(self, name, df):
        def target():
            self.histograms[name] = {
                c: histogram.plot_histogram(self.tables[name][c])
                for c in self.tables[name].columns
            }
            self._update_status(name, "done")
            self.widget.update(None, ["ColumnSummary"])
        
        self.eda_thread = threading.Thread(target=target)
        self.eda_thread.start()

    def _update_status(self, name, status):
        self.status_table.loc[self.status_table["name"]==name, "status"] = status


def _get_name():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
