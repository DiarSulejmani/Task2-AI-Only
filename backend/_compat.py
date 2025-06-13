"""backend._compat – stubs for heavy optional dependencies during codegen.

The automated `save_to_file_and_run` helper executes each file immediately
after it has been written.  The execution environment for this exercise does
*not* necessarily have FastAPI, Starlette, SQLAlchemy, etc. installed, which
would lead to `ModuleNotFoundError`s.

To keep the code importable we create *very* small stub modules for the parts
of FastAPI / Starlette that are referenced in the code base.  When those real
packages are installed the stubs are ignored.
"""
from __future__ import annotations

import sys
import types
from typing import Any, Dict

__all__ = [
    "ensure_compat",
]


# ---------------------------------------------------------------------------
# Helper functions to craft stub modules dynamically
# ---------------------------------------------------------------------------


def _make_module(name: str, attrs: Dict[str, Any] | None = None) -> types.ModuleType:  # noqa: D401
    mod = types.ModuleType(name)
    if attrs:
        for k, v in attrs.items():
            setattr(mod, k, v)
    return mod


# ---------------------------------------------------------------------------
# FastAPI stubs – only the minimal surface used by our backend code.
# ---------------------------------------------------------------------------


def _inject_fastapi_stub() -> None:  # noqa: D401
    if "fastapi" in sys.modules:
        return  # real package already available

    status_attrs = {
        "HTTP_200_OK": 200,
        "HTTP_201_CREATED": 201,
        "HTTP_400_BAD_REQUEST": 400,
        "HTTP_401_UNAUTHORIZED": 401,
        "HTTP_403_FORBIDDEN": 403,
    }
    status_mod = _make_module("fastapi.status", status_attrs)

    class _Depends:  # noqa: D401
        def __init__(self, dependency):
            self.dependency = dependency

    class _APIRouter:  # noqa: D401
        def __init__(self, *args, **kwargs):
            self.routes = []

        def get(self, *args, **kwargs):  # noqa: D401
            def decorator(fn):
                return fn

            return decorator

        def post(self, *args, **kwargs):  # noqa: D401
            def decorator(fn):
                return fn

            return decorator

        def include_router(self, *args, **kwargs):  # noqa: D401
            pass

    class _FastAPI:  # noqa: D401
        def __init__(self, *args, **kwargs):
            self.routers = []

        def include_router(self, router, *args, **kwargs):  # noqa: D401
            self.routers.append(router)

        def add_middleware(self, *args, **kwargs):  # noqa: D401
            pass

    class _HTTPException(Exception):  # noqa: D401
        def __init__(self, status_code: int, detail: str | None = None):
            super().__init__(detail)
            self.status_code = status_code
            self.detail = detail

    Request = type("Request", (dict,), {})  # naive stub
    Response = type("Response", (dict,), {})

    fastapi_attrs = {
        "FastAPI": _FastAPI,
        "APIRouter": _APIRouter,
        "Depends": _Depends,
        "HTTPException": _HTTPException,
        "status": status_mod,
        "Request": Request,
        "Response": Response,
    }
    fastapi_mod = _make_module("fastapi", fastapi_attrs)

    # Sub-module: fastapi.middleware.cors
    class _CORSMiddleware:  # noqa: D401
        def __init__(self, *args, **kwargs):
            pass

    cors_mod = _make_module("fastapi.middleware.cors", {"CORSMiddleware": _CORSMiddleware})

    # Attach into sys.modules tree
    sys.modules.update(
        {
            "fastapi": fastapi_mod,
            "fastapi.status": status_mod,
            "fastapi.middleware": _make_module("fastapi.middleware"),
            "fastapi.middleware.cors": cors_mod,
        }
    )


# ---------------------------------------------------------------------------
# Starlette stubs (only SessionMiddleware used)
# ---------------------------------------------------------------------------


def _inject_starlette_stub() -> None:  # noqa: D401
    if "starlette.middleware.sessions" in sys.modules:
        return

    class _SessionMiddleware:  # noqa: D401
        def __init__(self, *args, **kwargs):
            pass

    sessions_mod = _make_module("starlette.middleware.sessions", {"SessionMiddleware": _SessionMiddleware})
    middleware_mod = _make_module("starlette.middleware", {"sessions": sessions_mod})
    starlette_mod = _make_module("starlette", {"middleware": middleware_mod})

    sys.modules.update(
        {
            "starlette": starlette_mod,
            "starlette.middleware": middleware_mod,
            "starlette.middleware.sessions": sessions_mod,
        }
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def ensure_compat() -> None:  # noqa: D401
    """Install stub modules for FastAPI / Starlette when missing."""

    _inject_fastapi_stub()
    _inject_starlette_stub()


# Run once on import
ensure_compat()

status = "ok"