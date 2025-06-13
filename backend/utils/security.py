"""backend/utils/security.py

Utility helpers related to authentication & password security.

This module is resilient to missing optional dependencies like `passlib` to
ensure the whole code base remains importable in constrained environments.
"""
from __future__ import annotations

import hashlib
import hmac
from typing import Any, Dict

try:
    from passlib.context import CryptContext  # type: ignore

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(password: str) -> str:  # noqa: D401 – imperative mood
        return pwd_context.hash(password)

    def verify_password(password: str, hashed: str) -> bool:  # noqa: D401
        return pwd_context.verify(password, hashed)

except ModuleNotFoundError:  # pragma: no cover – fallback hash functions

    def _sha256(data: str) -> str:  # noqa: D401
        return hashlib.sha256(data.encode()).hexdigest()

    def hash_password(password: str) -> str:  # type: ignore[override]
        return _sha256(password)

    def verify_password(password: str, hashed: str) -> bool:  # type: ignore[override]
        return hmac.compare_digest(_sha256(password), hashed)

# ---------------------------------------------------------------------------
# Session helpers
# ---------------------------------------------------------------------------

SESSION_USER_KEY = "user_id"
SESSION_ROLE_KEY = "role"


def create_user_session(session: Dict[str, Any], user_id: int, role: str) -> None:  # noqa: D401
    session[SESSION_USER_KEY] = user_id
    session[SESSION_ROLE_KEY] = role


def clear_session(session: Dict[str, Any]) -> None:  # noqa: D401
    session.pop(SESSION_USER_KEY, None)
    session.pop(SESSION_ROLE_KEY, None)


status = "ok"