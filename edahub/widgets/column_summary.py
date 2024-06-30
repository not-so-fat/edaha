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
            with stats:
                display(HTML(self._get_table_html(table_name, edahub.stats_tables[table_name])))
            histogram_columns = list(edahub.histograms[table_name].keys()) if table_name in edahub.histograms \
                    else []
            if histogram_columns:
                histogram_stack = widgets.Stack(
                    [widgets.Output(layout=widgets.Layout(width='100%')) for c in histogram_columns],
                    selected_index=0
                )
                for i, c in enumerate(histogram_columns):
                    with histogram_stack.children[i]:
                        histogram_stack.children[i].clear_output()
                        display(edahub.histograms[table_name][c])
                select_chart, filter_text = self._get_histogram_selection(
                    table_name, edahub, histogram_columns, histogram_stack
                )

                contents.append(
                    widgets.VBox([stats, widgets.HBox([select_chart, filter_text]), histogram_stack])
                )
            else:
                contents.append(widgets.VBox([stats]))

        self.output.children = contents
        for i, title in enumerate(table_names):
            self.output.set_title(i, title)

    def reset_search_box(self):
        for table_view in self.output.children:
            if len(table_view.children) > 1: # has histogram module
                table_view.children[1].children[1].value = ""
                table_view.children[1].children[0].index = 0 # for the case histogram is unselected by search

    def _get_table_html(self, table_name, table_df):
        return table_df.to_html()

    def _get_histogram_selection(self, table_name, edahub, histogram_columns, histogram_stack):
        select_chart = widgets.Dropdown(
            options=histogram_columns,
            description='Select Chart:',
            value=histogram_columns[0], # None would be better to make it consistent with search box, but having default value ensure exported html will include chart
            disabled=False
        )
        filter_text = widgets.Text(
            placeholder='',
            description='Type to filter:',
            disabled=False
        )

        def filter_options(text):
            filtered_options = [option for option in histogram_columns if text.lower() in option.lower()]
            select_chart.options = filtered_options

        def handle_text_change(change):
            filter_options(change['new'])

        filter_text.observe(handle_text_change, names='value')
        widgets.jslink((select_chart, 'index'), (histogram_stack, 'selected_index'))
        return select_chart, filter_text
