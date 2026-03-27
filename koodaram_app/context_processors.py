from __future__ import annotations

from typing import Any

from django.conf import settings
from .models import CampingPackage


def _star_parts(rating: float) -> list[str]:
    rating = max(0.0, min(5.0, float(rating)))
    full = int(rating)
    remainder = rating - full
    half = 1 if remainder >= 0.25 and remainder < 0.75 else 0
    if remainder >= 0.75:
        full = min(5, full + 1)
    empty = max(0, 5 - full - half)
    return (["full"] * full) + (["half"] * half) + (["empty"] * empty)


def google_reviews(request) -> dict[str, Any]:
    rating = getattr(settings, "GOOGLE_REVIEW_RATING", 0.0)
    count = getattr(settings, "GOOGLE_REVIEW_COUNT", 0)
    url = getattr(settings, "GOOGLE_REVIEW_URL", "")
    return {
        "google_review_rating": rating,
        "google_review_count": count,
        "google_review_url": url,
        "google_review_stars": _star_parts(rating),
    }


def footer_packages(request) -> dict[str, Any]:
    packages = CampingPackage.objects.only("name", "slug").order_by("-created_at")[:5]
    return {"footer_packages": packages}
