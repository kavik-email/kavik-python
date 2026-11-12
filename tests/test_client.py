"""Unit tests for the Kavik client's defaults and public names. No network:
requests go to an httpx.MockTransport. Run from sdk/python with
``py -3 -m pytest tests/test_client.py``."""

import httpx
import pytest

import kavikemail
from kavikemail import Kavik, KavikError, NotFoundError


def _recording(kv, status=200, body=None):
    """Point ``kv`` at a transport that answers every request with
    ``status``/``body`` and return the list of requests it saw."""
    seen = []

    def handler(req: httpx.Request) -> httpx.Response:
        seen.append(req)
        return httpx.Response(status, json={"data": []} if body is None else body)

    kv._client = httpx.Client(transport=httpx.MockTransport(handler))
    return seen


def test_bare_key_talks_to_api_kavik_email():
    kv = Kavik("eva_test")
    seen = _recording(kv)
    kv.list_bulk_jobs()
    assert str(seen[0].url) == "https://api.kavik.email/api/v1/verify/async"


def test_base_url_with_api_v1_is_accepted():
    kv = Kavik("eva_test", base_url="https://api.kavik.email/api/v1/")
    seen = _recording(kv)
    kv.list_bulk_jobs()
    assert str(seen[0].url) == "https://api.kavik.email/api/v1/verify/async"


def test_missing_key_raises():
    with pytest.raises(ValueError, match="api_key is required"):
        Kavik("")


def test_api_errors_are_kavik_errors():
    kv = Kavik("eva_test", max_retries=0)
    _recording(kv, 404, {"error": "not found", "code": "NOT_FOUND"})
    with pytest.raises(NotFoundError) as exc:
        kv.get_bulk_job("x")
    assert isinstance(exc.value, KavikError)


def test_public_names_carry_no_old_brand():
    assert {"Kavik", "KavikError", "KavikResponse"} <= set(kavikemail.__all__)
    # No export keeps the old client prefix (the old names all began "Ev").
    assert not [n for n in kavikemail.__all__ if n.lower().startswith("ev")]
