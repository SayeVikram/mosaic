# Mosaic Widget

[![PyPi](https://img.shields.io/pypi/v/mosaic-widget.svg)](https://pypi.org/project/mosaic-widget/)

A Jupyter widget for Mosaic. Given a declarative specification, will generate web-based visualizations while leveraging DuckDB in the Jupyter kernel. Create interactive Mosaic plots over Pandas and Polars data frames or DuckDB connections.

Learn how to install and use the widget in the [Mosaic documentation](https://uwdata.github.io/mosaic/jupyter/).

## Fluent Python API (experimental)

In addition to authoring specs as raw dicts, `mosaic-widget` includes an Altair-inspired fluent API that compiles to a Mosaic spec dict:

```python
from mosaic_widget import (
    chart,
    from_,
    ref,
    dateMonthDay,
    intervalX,
    highlight,
    colorLegend,
)

c = (
    chart("weather")
    .mark_dot(data=from_("weather", filterBy=ref("click")))
    .encode(x=dateMonthDay("date"), y="temp_max", fill="weather", fillOpacity=0.7)
    .properties(width=680, height=300)
    .add_selection(colorLegend(as_="click", columns=1))
    .add_selection(intervalX("range", brush={"fill": "none", "stroke": "#888"}))
    .add_selection(highlight(by="range", fill="#ccc", fillOpacity=0.2))
)

spec = c.to_spec()
widget = c.widget()  # or: c.widget(data={"weather": your_dataframe})
widget
```

## Developer Setup

We use [uv](https://docs.astral.sh/uv/) to manage our development setup.

You can start Jupyter with `ANYWIDGET_HMR=1 uv run jupyter lab --notebook-dir=../../dev/notebooks`.

Run `npm run build` to build the widget JavaScript code. If you want to live edit the widget code, run `npm run dev` in a separate terminal.

Run `uv run ruff check --fix` and `uv run ruff format` to lint the code.

## Publishing

Run the build with `uv build`. Then publish with `uvx twine upload --skip-existing dist/*`. We publish using tokens so when asked, set the username to `__token__` and then use your token as the password. Alternatively, create a [`.pypirc` file](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#create-an-account).
