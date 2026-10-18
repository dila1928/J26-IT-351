"""
Minimal Firestore REST client for the backend's auto-log feature.

Deliberately avoids the `firebase-admin` / `google-cloud-firestore` SDKs:
those pull in a protobuf version that conflicts with the TensorFlow
version this backend already depends on (RGB/Thermal services). Instead
this talks to the Firestore REST API directly, authenticated with
`google-auth` (no protobuf dependency), using the same service-account
key the mobile app's Firebase project already trusts.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account

BASE_DIR = Path(__file__).resolve().parent.parent.parent

_SCOPES = ["https://www.googleapis.com/auth/datastore"]
_DEFAULT_CREDENTIALS_PATH = BASE_DIR / "smartbellpaper-ai-firebase-adminsdk-fbsvc-69ed7640f8.json"

_credentials: service_account.Credentials | None = None
_project_id: str | None = None


def _credentials_path() -> Path:
    return Path(os.environ.get("FIREBASE_CREDENTIALS_PATH", str(_DEFAULT_CREDENTIALS_PATH)))


def _load_credentials() -> service_account.Credentials:
    global _credentials, _project_id
    if _credentials is None:
        path = _credentials_path()
        if not path.exists():
            raise RuntimeError(f"Firebase service account key not found at {path}")
        _credentials = service_account.Credentials.from_service_account_file(str(path), scopes=_SCOPES)
        _project_id = _credentials.project_id
    return _credentials


def _access_token() -> str:
    creds = _load_credentials()
    if not creds.valid:
        creds.refresh(Request())
    return creds.token


def _documents_url(collection: str, doc_id: str | None = None) -> str:
    path = f"projects/{_project_id}/databases/(default)/documents/{collection}"
    if doc_id:
        path += f"/{doc_id}"
    return f"https://firestore.googleapis.com/v1/{path}"


def _to_firestore_value(value: Any) -> dict:
    if value is None:
        return {"nullValue": None}
    if isinstance(value, bool):
        return {"booleanValue": value}
    if isinstance(value, int):
        return {"integerValue": str(value)}
    if isinstance(value, float):
        return {"doubleValue": value}
    if isinstance(value, str):
        return {"stringValue": value}
    if isinstance(value, dict):
        return {"mapValue": {"fields": {k: _to_firestore_value(v) for k, v in value.items()}}}
    if isinstance(value, (list, tuple)):
        return {"arrayValue": {"values": [_to_firestore_value(v) for v in value]}}
    return {"stringValue": str(value)}


def _from_firestore_value(value: dict) -> Any:
    if "nullValue" in value:
        return None
    if "booleanValue" in value:
        return value["booleanValue"]
    if "integerValue" in value:
        return int(value["integerValue"])
    if "doubleValue" in value:
        return value["doubleValue"]
    if "stringValue" in value:
        return value["stringValue"]
    if "timestampValue" in value:
        return value["timestampValue"]
    if "mapValue" in value:
        return {k: _from_firestore_value(v) for k, v in value.get("mapValue", {}).get("fields", {}).items()}
    if "arrayValue" in value:
        return [_from_firestore_value(v) for v in value.get("arrayValue", {}).get("values", [])]
    return None


def add_document(collection: str, fields: dict) -> dict:
    """Adds an auto-ID document to `collection`. Returns {id, ...fields}."""
    _load_credentials()
    url = _documents_url(collection)
    body = {"fields": {k: _to_firestore_value(v) for k, v in fields.items()}}
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {_access_token()}", "Content-Type": "application/json"},
        json=body,
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    doc_id = data["name"].rsplit("/", 1)[-1]
    return {"id": doc_id, **{k: _from_firestore_value(v) for k, v in data.get("fields", {}).items()}}
