"""Unit tests for the result parser. No network. Run from sdk/python with
``py -3 -m pytest tests/test_models.py`` (tests/test_live.py needs a live API
and exits at import without KAVIK_API_KEY, so name this file explicitly)."""

from kavik.models import parse_bulk_job_result, parse_verification_result

BASE = {
    "email": "karl@t-online.de",
    "score": 45,
    "risk": "risky",
    "syntax_valid": True,
    "mx_found": True,
    "smtp_check": "risky",
    "reason": "account_recovery",
    "is_disposable": False,
    "is_role_account": False,
    "is_catch_all": False,
    "is_free_provider": True,
    "spam_trap_risk": "low",
    "mx_records": ["mx00.t-online.de"],
}


def test_parse_is_locked():
    result = parse_verification_result({**BASE, "is_locked": True})
    assert result.is_locked is True
    assert result.reason == "account_recovery"
    assert result.score == 45


def test_parse_is_locked_absent_is_none():
    assert parse_verification_result(BASE).is_locked is None


def test_parse_ignores_unknown_keys():
    # A payload may carry keys this version does not know; they are dropped.
    result = parse_verification_result({**BASE, "some_new_field": True})
    assert not hasattr(result, "some_new_field")
    assert result.score == 45


BULK_ROW = {
    "email": "karl@t-online.de",
    "score": 45,
    "risk": "risky",
    "smtp_check": "risky",
    "is_disposable": False,
    "is_role_account": False,
    "is_catch_all": False,
    "is_free_provider": True,
    "spam_trap_risk": "low",
}


def test_parse_bulk_job_result_is_locked():
    assert parse_bulk_job_result({**BULK_ROW, "is_locked": True}).is_locked is True


def test_parse_bulk_job_result_is_locked_absent_is_none():
    # Rows from jobs that finished before the column existed carry no key.
    assert parse_bulk_job_result(BULK_ROW).is_locked is None
