# EDAHub
## What is this?

EDA (exploratory data analysis) results can be more structured.

EDAHub provides a lightweight dashboard for you to review your data summary on the side screen in JupyterLab, making it easier and quicker to revisit.
![Screenshot](assets/readme_example.png)


## Why this is useful?
As a data scientist, I've seen many notebooks that mix data/ML pipeline logic with observations. EDAHub addresses this by organizing basic observations in one place.

## How to start

### Install
You can try it on your JupyterLab with pip install:

```bash
pip install edahub
```

### Whole example
![Example notebook](examples/edahub_example.ipynb) would help you to understand how it works.

### Quick start

After instantiating "EDAHub" object, you can load your pandas.DataFrame with name:

```
import edahub
eda = edahub.EDAHub()

eda.add_table("<your table name>", df)
```

You will see the widget on the right side.


Also you can register charts you developed into the dashboard:

```
chart1 = ...
chart2 = ...
eda.add_chart("<name of section>", chart1)
eda.add_chart("<name of section>", chart2)
```
It will display your chart on the tab "Charts"

You can save widget as html file, you can open it on the browser independently on Jupyter.

```
eda.export_html("edahub_export.html")
```

NOTE: I observe instability in updating output of widgets. When output doesn't look right, please click "Update" button to update the widget.
