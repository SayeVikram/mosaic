from __future__ import annotations

from .chart import (
    Chart,
    avg_,
    bin,
    chart,
    count,
    dateMonthDay,
    from_,
    max_,
    min_,
    ref,
    sql,
    sum_,
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
