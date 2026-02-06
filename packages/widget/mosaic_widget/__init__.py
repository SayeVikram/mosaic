from __future__ import annotations

from .chart import (
    Chart,
    Directive,
    avg_,
    bin,
    chart,
    colorLegend,
    count,
    crossfilter,
    dateMonthDay,
    from_,
    highlight,
    intersect,
    intervalX,
    intervalXY,
    intervalY,
    max_,
    min_,
    ref,
    single,
    sql,
    sum_,
    toggleY,
)

# re-exporting the widget so past versions could still work
try:
    from .widget import MosaicWidget  
except ModuleNotFoundError as _err: 
    
    class MosaicWidget: 
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "dependencies not installed. "
                "Install dependencies."
            ) from _err
