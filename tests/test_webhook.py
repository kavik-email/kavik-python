"""Unit tests for webhook signature checks. Run from sdk/python with
``py -3 -m pytest tests/test_webhook.py``."""

import hashlib
import hmac

from kavik import verify_webhook_signature

SECRET = "whsec_test"
BODY = b'{"event":"job.completed","job_id":"j1"}'
SIGNATURE = hmac.new(SECRET.encode(), BODY, hashlib.sha256).hexdigest()


def test_bytes_and_str_payloads_verify():
    assert verify_webhook_signature(BODY, SIGNATURE, SECRET) is True
    assert verify_webhook_signature(BODY.decode(), SIGNATURE, SECRET) is True


def test_wrong_signature_fails():
    assert verify_webhook_signature(BODY, "0" * 64, SECRET) is False


def test_missing_signature_header_is_a_failed_check_not_a_crash():
    # request.headers.get("X-EVA-Signature") is None when the header is absent.
    assert verify_webhook_signature(BODY, None, SECRET) is False
