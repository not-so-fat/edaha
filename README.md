# EDAHub
## What is this?

EDA (exploratory data analysis) results can be more structured.

EDAHub provides a side screen in JupyterLab to summarize your data, making it easier and quicker to revisit.
![Screenshot](assets/screenshot.png)


## Why this is useful?
As a data scientist, I've seen many notebooks that mix data/ML pipeline logic with observations. EDAHub addresses this by organizing basic observations in one place.

## How to start
You can try it on your JupyterLab with pip install:

```bash
pip install edahub
```

then add your pandas.DataFrame with name:

```
import edahub
eda = edahub.EDAHub()

eda.add_table("customers", df)
```

You will see the widget on the right side.
