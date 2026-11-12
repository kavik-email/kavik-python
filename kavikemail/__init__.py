"""Kavik.email API: official Python SDK.

Example::

    from kavikemail import Kavik

    kavik = Kavik("eva_...")
    result = kavik.verify("user@example.com")
    print(result.data.risk, result.data.score)
"""

from .client import Kavik
from .errors import (
    AuthenticationError,
    DailyLimitError,
    KavikError,
    NotFoundError,
    QuotaExceededError,
    RateLimitError,
    WebhookSignatureError,
)
from .models import (
    BatchResult,
    BlacklistEntry,
    BlacklistResult,
    BulkJob,
    BulkJobCompletedEvent,
    BulkJobResult,
    DKIMResult,
    DMARCResult,
    DomainAuth,
    DomainDeliverability,
    KavikResponse,
    RateLimitInfo,
    SPFResult,
    VerificationResult,
    WebhookSummary,
)
from .webhook import parse_webhook_event, verify_webhook_signature

__all__ = [
    # Client
    "Kavik",
    # Models
    "BatchResult",
    "BlacklistEntry",
    "BlacklistResult",
    "BulkJob",
    "BulkJobCompletedEvent",
    "BulkJobResult",
    "DKIMResult",
    "DMARCResult",
    "DomainAuth",
    "DomainDeliverability",
    "KavikResponse",
    "RateLimitInfo",
    "SPFResult",
    "VerificationResult",
    "WebhookSummary",
    # Errors
    "AuthenticationError",
    "DailyLimitError",
    "KavikError",
    "NotFoundError",
    "QuotaExceededError",
    "RateLimitError",
    "WebhookSignatureError",
    # Webhook utilities
    "parse_webhook_event",
    "verify_webhook_signature",
]
