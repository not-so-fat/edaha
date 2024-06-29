import ipywidgets as widgets
from IPython.display import display, HTML

from ..logic.vis import histogram


class EDAHubWidgetCustom:
    def __init__(self):
        self.output = widgets.Accordion()

    def update(self, edahub):
        groups = list(edahub.custom_objs.keys())
        contents = []
        for group in groups:
            output = widgets.Output(layout=widgets.Layout(width='100%'))
            with output:
                for obj in edahub.custom_objs[group]:
                    display(obj)
            contents.append(output)
        self.output.children = contents
        for i, group in enumerate(groups):
            self.output.set_title(i, group)
