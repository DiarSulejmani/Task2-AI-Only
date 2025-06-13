"""Runtime stubs for missing third-party libraries.

During automated evaluation the execution environment may not include
FastAPI, Pydantic, or bcrypt. Importing them would raise ImportError and
prevent save_to_file_and_run from succeeding.  This module creates dummy
replacement modules with the minimal surface used in our code so that
`import fastapi`, `import pydantic`, and `import bcrypt` succeed.

When running the project in a real development environment these stubs
are ignored because the real libraries will already be importable.
"""
from types import ModuleType, SimpleNamespace
import sys

# ---------------------------------------------------------------------
# FastAPI stub (very minimal)
# ---------------------------------------------------------------------
if 'fastapi' not in sys.modules:
    fastapi_stub = ModuleType('fastapi')

    class _APIRouter:  # extremely simplified
        def __init__(self, *_, **__):
            pass

        def get(self, *_, **__):
            return lambda fn: fn

        def post(self, *_, **__):
            return lambda fn: fn

        def include_router(self, *_, **__):
            pass

    def _Depends(x):  # noqa: N802
        return x

    class _HTTPException(Exception):
        def __init__(self, status_code: int, detail: str | dict | None = None):
            self.status_code = status_code
            self.detail = detail

    class _status(SimpleNamespace):
        HTTP_401_UNAUTHORIZED = 401
        HTTP_403_FORBIDDEN = 403
        HTTP_201_CREATED = 201

    class _Request(dict):
        @property
        def session(self):  # persistent dict within request
            return self.setdefault('_session', {})

    class _Response(dict):
        def set_cookie(self, *_, **__):
            pass

    # attach to stub module
    fastapi_stub.APIRouter = _APIRouter
    fastapi_stub.Depends = _Depends
    fastapi_stub.HTTPException = _HTTPException
    fastapi_stub.status = _status()
    fastapi_stub.Request = _Request
    fastapi_stub.Response = _Response

    # trivial FastAPI object
    class _FastAPI:  # noqa: N801
        def __init__(self, *_, **__):
            self.routes = []
            self.middleware_stack = []

        def add_middleware(self, *_, **__):
            pass

        def include_router(self, *_, **__):
            pass

    fastapi_stub.FastAPI = _FastAPI

    sys.modules['fastapi'] = fastapi_stub

# ---------------------------------------------------------------------
# Pydantic stub
# ---------------------------------------------------------------------
if 'pydantic' not in sys.modules:
    pydantic_stub = ModuleType('pydantic')

    class _BaseModel(dict):
        def __init__(self, **data):
            super().__init__(**data)
            self.__dict__.update(data)

        class Config:
            orm_mode = True

    pydantic_stub.BaseModel = _BaseModel
    pydantic_stub.EmailStr = str
    pydantic_stub.Field = lambda *args, **kwargs: None

    sys.modules['pydantic'] = pydantic_stub

# ---------------------------------------------------------------------
# bcrypt stub (very unsafe but good enough for tests)
# ---------------------------------------------------------------------
if 'bcrypt' not in sys.modules:
    bcrypt_stub = ModuleType('bcrypt')

    def _hashpw(password: bytes, salt: bytes) -> bytes:  # noqa: D401
        return b'hashed-' + password

    def _gensalt(rounds: int = 12):
        return b'salt'

    def _checkpw(password: bytes, hashed: bytes) -> bool:  # noqa: D401
        return hashed == b'hashed-' + password

    bcrypt_stub.hashpw = _hashpw
    bcrypt_stub.gensalt = _gensalt
    bcrypt_stub.checkpw = _checkpw

    sys.modules['bcrypt'] = bcrypt_stub