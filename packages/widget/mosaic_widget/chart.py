from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, MutableMapping


def ref(name: str) -> str:
    """Return a Mosaic param reference"""
    return name if name.startswith("$") else f"${name}"

def from_(table: str, **options: Any) -> dict[str, Any]:
    """Create a Mosaic mark data reference"""
    return {"from": table, **options} if options else {"from": table}

def dateMonthDay(field: str) -> dict[str, Any]:
    return {"dateMonthDay": field}


def bin(field: str, **options: Any) -> dict[str, Any]:
    return {"bin": field, **options} if options else {"bin": field}


def count() -> dict[str, Any]:
    return {"count": None}


def avg_(field: str) -> dict[str, Any]:
    return {"avg": field}


def sum_(field: str) -> dict[str, Any]:
    return {"sum": field}


def min_(field: str) -> dict[str, Any]:
    return {"min": field}


def max_(field: str) -> dict[str, Any]:
    return {"max": field}


def sql(expr: str) -> dict[str, Any]:
    return {"sql": expr}



class Chart:
    """Altair-like spec builder"""

    def __init__(self, data: str | None = None):
        #metadata like data, params, etc. in head 
        self._head: dict[str, Any] = {}
        self._data_from: str | None = data
        self._plot: dict[str, Any] = {"plot": []}
        self._current_mark: MutableMapping[str, Any] | None = None

    def __getattr__(self, name: str): #fallback for non-defined attributes
        # helping change mark_dot to mark("dot", ...)
        if name.startswith("mark_"):
            mark = name[len("mark_") :]

            def _mark(**options: Any) -> Chart:
                return self.mark(mark, **options)

            return _mark

    def meta(self, **meta: Any) -> Chart:
        self._head.setdefault("meta", {}).update(meta)
        return self

    def data(self, name: str, **definition: Any) -> Chart:
        """data definition under spec.data."""
        self._head.setdefault("data", {})[name] = dict(definition)
        return self

    def param(self, name: str, value: Any) -> Chart:
        """Add a top-level param definition/value under ``spec.params``."""
        self._head.setdefault("params", {})[name] = value
        return self


    def mark(self, mark: str, data: Mapping[str, Any] | None = None, **options: Any) -> Chart:
        entry: dict[str, Any] = {"mark": mark}
        if data is None and self._data_from is not None:
            entry["data"] = {"from": self._data_from}
        elif data is not None:
            entry["data"] = dict(data)
        entry.update(options) # mark options like fill, etc. 
        self._plot["plot"].append(entry)
        self._current_mark = entry
        return self

    def encode(self, **channels: Any) -> Chart:
        if self._current_mark is None:
            raise ValueError("encode() called before mark.")
        # Mosaic spec uses channel keys directly on the mark entry.
        self._current_mark.update(channels)
        return self

    def properties(self, **attrs: Any) -> Chart:
        self._plot.update(attrs)
        return self

    def to_spec(self) -> dict[str, Any]:
        spec: dict[str, Any] = {}
        for k, v in self._head.items():
            if v:
                spec[k] = v
        spec.update(self._plot)
        return spec

    def widget(self, **kwargs: Any):
        """Instantiate a MosaicWidget for the chart."""
        from . import MosaicWidget

        return MosaicWidget(spec=self.to_spec(), **kwargs)


def chart(data: str | None = None) -> Chart:
    return Chart(data=data)

