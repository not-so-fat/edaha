import ipywidgets as widgets
from IPython.display import display, HTML

from ..logic.vis import histogram


class EDAHubWidgetColumnSummary:
    def __init__(self):
        self.output = widgets.Accordion()

    def update(self, edahub):
        table_names = edahub.get_table_names()
        contents = []
        for table_name in table_names:
            stats = widgets.Output(layout=widgets.Layout(width='100%'))
            histogram = widgets.Output(layout=widgets.Layout(width='100%'))
            select_chart, filter_text = self._get_histogram_selection(table_name, edahub, histogram)

            with stats:
                display(HTML(self._get_table_html(table_name, edahub.stats_tables[table_name])))
            contents.append(
                widgets.VBox(
                    [
                        stats, 
                        widgets.HBox([select_chart, filter_text]),
                        histogram
                    ]
                )
            )

        self.output.children = contents
        for i, title in enumerate(table_names):
            self.output.set_title(i, title)

    def _get_table_html(self, table_name, table_df):
        return table_df.to_html()

    def _get_histogram_selection(self, table_name, edahub, histogram):
        available_columns = list(edahub.histograms[table_name].keys()) if table_name in edahub.histograms \
            else []
        select_chart = widgets.Select(
            options=available_columns,
            description='Select Chart:',
            value=None,
            disabled=False
        )
        filter_text = widgets.Text(
            placeholder='',
            description='Type to filter:',
            disabled=False
        )

        def update_chart(change):
            column_name = change['new']
            chart = edahub.histograms[table_name].get(column_name)
            if chart:
                with histogram:
                    histogram.clear_output()
                    display(chart)

        def filter_options(text):
            filtered_options = [option for option in available_columns if text.lower() in option.lower()]
            select_chart.options = filtered_options

        def handle_text_change(change):
            filter_options(change['new'])

        select_chart.observe(update_chart, names='value')
        filter_text.observe(handle_text_change, names='value')
        return select_chart, filter_text
