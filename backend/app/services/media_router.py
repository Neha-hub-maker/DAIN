"""
Media Router Service
Routes approved press kits to the appropriate distribution channels
across 4 network tiers based on domain, achievement magnitude, and content type.

Network Tiers:
  1. National   — High-tier: funding ≥ $50k, major research, venture exits
  2. Byte Size  — Quick social highlights: CGPA, skills, minor personal milestones
  3. Campus     — University-oriented: research, student volunteering, campus initiatives
  4. News/Blogs — Standard press: corporate roles, industry placements, general ventures
"""

from typing import Any


# ──────────────────────────────────────────────────────────────
# Channel definitions per tier
# ──────────────────────────────────────────────────────────────

TIER_CHANNELS: dict[str, list[str]] = {
    "National": [
        "National Press Wire",
        "Industry Publication Syndicate",
        "Major News Outlet Distribution",
    ],
    "Byte Size": [
        "Social Media Highlight Feed",
        "Short-Form Content Platform",
        "Community Digest Newsletter",
    ],
    "Campus": [
        "University News Board",
        "Student Association Bulletin",
        "Campus Research Digest",
    ],
    "News/Blogs": [
        "Tech Blog Network",
        "Industry Blog Syndicate",
        "General Press Release Wire",
    ],
}


# ──────────────────────────────────────────────────────────────
# Domain-specific routing rules
# ──────────────────────────────────────────────────────────────

def _safe_float(value: Any, fallback: float = 0.0) -> float:
    """Safely convert a value to float."""
    if value is None:
        return fallback
    try:
        return float(value)
    except (ValueError, TypeError):
        return fallback


def _safe_str(value: Any, fallback: str = "") -> str:
    """Safely convert a value to string, avoiding 'None'."""
    if value is None:
        return fallback
    s = str(value).strip()
    return s if s and s.lower() != "none" else fallback


def _route_academic(details: dict[str, Any]) -> list[str]:
    """Route academic milestones based on type and context."""
    milestone_type = _safe_str(details.get("type"))
    tiers = []

    # Research publications with strong institutional backing go National
    if milestone_type == "publication":
        tiers.append("National")
        tiers.append("Campus")
    elif milestone_type == "research":
        tiers.append("Campus")
        tiers.append("News/Blogs")
    elif milestone_type == "cgpa":
        tiers.append("Byte Size")
        tiers.append("Campus")
    else:
        tiers.append("Byte Size")

    return tiers


def _route_professional(details: dict[str, Any]) -> list[str]:
    """Route professional milestones. Corporate roles go to News/Blogs by default."""
    industry = _safe_str(details.get("industry_sector"))
    tiers = ["News/Blogs"]

    # If a recognized high-profile sector, also push to National
    high_profile_sectors = {"finance", "fintech", "healthcare", "ai", "defense", "energy"}
    if industry.lower() in high_profile_sectors:
        tiers.insert(0, "National")

    return tiers


def _route_entrepreneurial(details: dict[str, Any]) -> list[str]:
    """Route entrepreneurial milestones. High funding or exits go National."""
    funding = _safe_float(details.get("funding_amount"))
    stage = _safe_str(details.get("stage"))
    tiers = []

    if funding >= 50_000 or stage == "exited":
        tiers.append("National")
    if stage in ("mvp", "ideation"):
        tiers.append("Campus")
    tiers.append("News/Blogs")

    return list(dict.fromkeys(tiers))  # deduplicate while preserving order


def _route_social_impact(details: dict[str, Any]) -> list[str]:
    """Route social impact milestones. Large-scale efforts go National."""
    hours = _safe_float(details.get("hours_volunteered"))
    initiatives = _safe_float(details.get("initiatives_led"))
    tiers = []

    if hours >= 100 or initiatives >= 5:
        tiers.append("National")
    tiers.append("Campus")
    tiers.append("Byte Size")

    return list(dict.fromkeys(tiers))


def _route_personal(details: dict[str, Any]) -> list[str]:
    """Route personal milestones. Generally Byte Size unless notable."""
    return ["Byte Size"]


_DOMAIN_ROUTERS = {
    "academic": _route_academic,
    "professional": _route_professional,
    "entrepreneurial": _route_entrepreneurial,
    "social-impact": _route_social_impact,
    "personal": _route_personal,
}


# ──────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────

def route_media_package(
    domain: str,
    details: dict[str, Any],
    press_kit: dict[str, Any],
) -> dict[str, Any]:
    """
    Determine target network tiers and channels for a press kit.
    Returns a routing result dict suitable for MediaRoutingResult serialization.
    """
    router_fn = _DOMAIN_ROUTERS.get(domain)
    if router_fn is None:
        raise ValueError(f"Unknown domain '{domain}' for media routing.")

    target_tiers = router_fn(details)

    # Collect the specific channels for each matched tier
    channels: list[str] = []
    for tier in target_tiers:
        channels.extend(TIER_CHANNELS.get(tier, []))

    return {
        "press_kit": press_kit,
        "target_tiers": target_tiers,
        "channels": channels,
        "generated_at": press_kit.get("generated_at", ""),
    }
