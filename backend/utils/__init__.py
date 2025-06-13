"""backend.utils package – helper utilities for DuoQuanto backend."""
from __future__ import annotations

# Re-export submodules for convenience
from importlib import import_module as _im

for _sub in ("security",):
    try:
        globals()[_sub] = _im(f"backend.utils.{_sub}")
    except ModuleNotFoundError:
        pass

__all__ = ["security"]

status = "ok"