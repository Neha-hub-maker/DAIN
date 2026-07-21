"""
Media Packager Service
Generates structured, media-ready press kit payloads from approved milestones.
All optional fields are handled gracefully—no KeyError or "None" strings.
Press kits are generated dynamically on-the-fly, not persisted in the database.
"""

from datetime import datetime, timezone
from typing import Any


def _safe(value: Any, fallback: str = "") -> str:
    """Return str(value) if truthy, else fallback. Never returns 'None'."""
    if value is None:
        return fallback
    s = str(value).strip()
    return s if s and s.lower() != "none" else fallback


# ──────────────────────────────────────────────────────────────
# Domain-specific headline and story generators
# ──────────────────────────────────────────────────────────────

def _academic_kit(details: dict[str, Any]) -> dict[str, str]:
    milestone_type = _safe(details.get("type"), "academic achievement")
    title = _safe(details.get("title"), "Untitled Milestone")
    institution = _safe(details.get("institution"), "an academic institution")
    value = _safe(details.get("value"))
    date = _safe(details.get("date"))
    description = _safe(details.get("description"))

    headline = f"Academic Milestone: {title}"
    summary = f"A {milestone_type} milestone has been achieved at {institution}."
    if value:
        summary += f" Key metric: {value}."

    story_parts = [
        f"{title} represents a significant {milestone_type} accomplishment at {institution}.",
    ]
    if value:
        story_parts.append(f"The recorded metric for this achievement is {value}.")
    if date:
        story_parts.append(f"This milestone was recorded on {date}.")
    if description:
        story_parts.append(description)

    return {
        "headline": headline,
        "executive_summary": summary,
        "detailed_story": " ".join(story_parts),
    }


def _professional_kit(details: dict[str, Any]) -> dict[str, str]:
    role = _safe(details.get("role"), "a professional role")
    company = _safe(details.get("company"), "a company")
    location = _safe(details.get("location"))
    industry = _safe(details.get("industry_sector"))
    start = _safe(details.get("start_date"))
    end = _safe(details.get("end_date"), "Present")
    description = _safe(details.get("description"))

    headline = f"Professional Placement: {role} at {company}"
    summary = f"A professional placement as {role} has been confirmed at {company}."
    if industry:
        summary += f" Industry sector: {industry}."

    story_parts = [
        f"This placement as {role} at {company} marks a key career milestone.",
    ]
    if location:
        story_parts.append(f"The position is based in {location}.")
    if start:
        story_parts.append(f"Employment period: {start} to {end}.")
    if description:
        story_parts.append(description)

    return {
        "headline": headline,
        "executive_summary": summary,
        "detailed_story": " ".join(story_parts),
    }


def _entrepreneurial_kit(details: dict[str, Any]) -> dict[str, str]:
    venture = _safe(details.get("venture_name"), "an unnamed venture")
    role = _safe(details.get("role"), "Founder")
    stage = _safe(details.get("stage"), "early stage")
    funding_raw = details.get("funding_amount")
    funding_amount = float(funding_raw) if funding_raw is not None else 0.0
    funding_source = _safe(details.get("funding_source"))
    launch_date = _safe(details.get("launch_date"))
    description = _safe(details.get("description"))

    headline = f"Entrepreneurial Venture: {venture}"
    summary = f"{venture} ({stage} stage) led by {role} has been approved for media distribution."
    if funding_amount > 0:
        summary += f" Funding secured: ${funding_amount:,.0f}."

    story_parts = [
        f"{venture} is currently in the {stage} stage under the leadership of {role}.",
    ]
    if funding_amount > 0:
        story_parts.append(f"The venture has secured ${funding_amount:,.0f} in funding.")
    if funding_source:
        story_parts.append(f"Funding source: {funding_source}.")
    if launch_date:
        story_parts.append(f"Launched on {launch_date}.")
    if description:
        story_parts.append(description)

    return {
        "headline": headline,
        "executive_summary": summary,
        "detailed_story": " ".join(story_parts),
    }


def _social_impact_kit(details: dict[str, Any]) -> dict[str, str]:
    organization = _safe(details.get("organization"), "a community organization")
    cause = _safe(details.get("cause_area"), "community service")
    role = _safe(details.get("role"), "Volunteer")
    hours_raw = details.get("hours_volunteered")
    hours = float(hours_raw) if hours_raw is not None else 0.0
    initiatives_raw = details.get("initiatives_led")
    initiatives = int(initiatives_raw) if initiatives_raw is not None else 0
    scale = _safe(details.get("scale_metric"))
    date = _safe(details.get("date"))
    description = _safe(details.get("description"))

    headline = f"Social Impact: {role} at {organization}"
    summary = f"A social impact contribution as {role} at {organization} in the {cause} space has been verified."
    if hours > 0:
        summary += f" Total volunteer hours: {hours:.0f}."

    story_parts = [
        f"This contribution as {role} at {organization} focuses on {cause}.",
    ]
    if hours > 0:
        story_parts.append(f"Total volunteer hours logged: {hours:.0f}.")
    if initiatives > 0:
        story_parts.append(f"Number of initiatives led: {initiatives}.")
    if scale:
        story_parts.append(f"Community reach: {scale}.")
    if date:
        story_parts.append(f"Recorded on {date}.")
    if description:
        story_parts.append(description)

    return {
        "headline": headline,
        "executive_summary": summary,
        "detailed_story": " ".join(story_parts),
    }


def _personal_kit(details: dict[str, Any]) -> dict[str, str]:
    category = _safe(details.get("category"), "personal")
    title = _safe(details.get("title"), "Untitled Achievement")
    date_achieved = _safe(details.get("date_achieved"))
    description = _safe(details.get("description"))

    headline = f"Personal Achievement: {title}"
    summary = f"A {category} milestone ({title}) has been verified and approved."

    story_parts = [
        f"{title} is a verified {category} achievement.",
    ]
    if date_achieved:
        story_parts.append(f"Achieved on {date_achieved}.")
    if description:
        story_parts.append(description)

    return {
        "headline": headline,
        "executive_summary": summary,
        "detailed_story": " ".join(story_parts),
    }


# ──────────────────────────────────────────────────────────────
# Domain dispatcher
# ──────────────────────────────────────────────────────────────

_DOMAIN_GENERATORS = {
    "academic": _academic_kit,
    "professional": _professional_kit,
    "entrepreneurial": _entrepreneurial_kit,
    "social-impact": _social_impact_kit,
    "personal": _personal_kit,
}


def generate_press_kit(
    domain: str,
    details: dict[str, Any],
    contact_name: str = "Default Profile User",
    contact_email: str = "developer@dain.local",
) -> dict[str, Any]:
    """
    Generate a complete press kit payload for an approved milestone.
    Handles null/missing optional fields gracefully.
    Returns a dict suitable for serialization into PressKitPayload.
    """
    generator = _DOMAIN_GENERATORS.get(domain)
    if generator is None:
        raise ValueError(f"Unknown domain '{domain}' for press kit generation.")

    kit_text = generator(details)

    # Build media assets list from any URL-like fields or description refs
    media_assets: list[str] = []
    for key in ("url", "project_url", "media_url", "link"):
        val = _safe(details.get(key))
        if val:
            media_assets.append(val)
    if not media_assets:
        media_assets.append("No supporting media assets provided.")

    return {
        "headline": kit_text["headline"],
        "executive_summary": kit_text["executive_summary"],
        "detailed_story": kit_text["detailed_story"],
        "media_assets": media_assets,
        "contact_info": {
            "name": contact_name,
            "email": contact_email,
            "domain": domain,
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
