import logging
import re
from typing import Literal, Type, List, Set, ClassVar
from urllib.parse import urlparse

import httpx
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# Allowlisted domains — agent can only fetch from these
ALLOWED_DOMAINS: Set[str] = {
    "skills.sh",
    "skillhub.club",
    "raw.githubusercontent.com",
    "api.github.com",
}

class WebFetchInput(BaseModel):
    action: Literal[
        "fetch_url",        # Fetch raw content from an allowed URL
        "search_skills_sh", # Search skills.sh for a topic
        "fetch_skill",      # Fetch a specific skill by name from skills.sh or skillhub
    ] = Field(..., description="Action to perform.")

    url: str | None = Field(
        default=None,
        description="Full URL to fetch. Required for 'fetch_url'."
    )
    topic: str | None = Field(
        default=None,
        description="Topic/keyword to search. Required for 'search_skills_sh'."
    )
    skill_name: str | None = Field(
        default=None,
        description="Skill name slug (e.g. 'code-review'). Required for 'fetch_skill'."
    )
    source: Literal["skills.sh", "skillhub.club"] = Field(
        default="skills.sh",
        description="Marketplace source for 'fetch_skill'."
    )
    owner: str | None = Field(
        default=None,
        description="Owner/collection on skills.sh (e.g. 'anthropics/skills'). Optional."
    )


class WebFetchTool(BaseTool):
    """
    Controlled HTTP fetch tool restricted to skill marketplaces.
    Used to discover and pull existing skills from skills.sh and skillhub.club
    before creating new skills from scratch.

    ALLOWED DOMAINS: skills.sh, skillhub.club, raw.githubusercontent.com

    USE THIS TO:
    - Search skills.sh for existing skills in a domain
    - Fetch full skill.md content from marketplaces
    - Adapt marketplace skills rather than writing from scratch
    """

    name: str = "web_fetch"
    description: str = (
        "Fetch content from skill marketplaces (skills.sh, skillhub.club). "
        "Actions: "
        "'fetch_url' → get raw content from an allowed URL; "
        "'search_skills_sh' → browse skills.sh for a topic; "
        "'fetch_skill' → get a specific skill by name from a marketplace. "
        "Always use this before creating a new skill — adapt, don't invent."
    )
    args_schema: Type[BaseModel] = WebFetchInput

    ALLOWED_DOMAINS: ClassVar[Set[str]] = ALLOWED_DOMAINS

    KNOWN_OWNERS: ClassVar[List[str]] = [
        "anthropics/skills",
        "obra/superpowers",
        "wshobson/agents",
        "vercel-labs/agent-skills",
        "coreyhaines31/marketingskills",
        "antfu/skills",
        "expo/skills",
    ]

    def _is_allowed(self, url: str) -> bool:
        try:
            domain = urlparse(url).netloc.lstrip("www.")
            return any(domain == d or domain.endswith("." + d) for d in ALLOWED_DOMAINS)
        except Exception:
            return False

    def _fetch(self, url: str, timeout: int = 15) -> str:
        if not self._is_allowed(url):
            return (
                f"❌ Domain not in allowlist. Allowed: {sorted(ALLOWED_DOMAINS)}\n"
                f"Requested: {url}"
            )
        try:
            headers = {"User-Agent": "skill-agent/1.0 (skill discovery bot)"}
            with httpx.Client(follow_redirects=True, timeout=timeout) as client:
                response = client.get(url, headers=headers)
                response.raise_for_status()

            content = response.text
            # Strip HTML tags if it's a webpage
            if "<html" in content.lower()[:200]:
                content = self._strip_html(content)

            # Truncate to 8000 chars to avoid context overflow
            if len(content) > 8000:
                content = content[:8000] + f"\n\n[TRUNCATED — {len(content)} total chars]"

            logger.info("Fetched %s (%d chars)", url, len(content))
            return f"# Content from: {url}\n\n{content}"

        except httpx.HTTPStatusError as e:
            return f"❌ HTTP {e.response.status_code}: {url}"
        except httpx.TimeoutException:
            return f"❌ Timeout fetching: {url}"
        except Exception as e:
            logger.exception("Fetch error: %s", e)
            return f"❌ Fetch error: {e}"

    def _strip_html(self, html: str) -> str:
        """Basic HTML stripping — removes tags, decodes common entities."""
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'&nbsp;', ' ', text)
        text = re.sub(r'&amp;', '&', text)
        text = re.sub(r'&lt;', '<', text)
        text = re.sub(r'&gt;', '>', text)
        text = re.sub(r'&quot;', '"', text)
        text = re.sub(r'\s{3,}', '\n\n', text)
        return text.strip()

    def _handle_search_skills_sh(self, topic: str) -> str:
        results = [f"# skills.sh — Search Results for: '{topic}'\n"]
        results.append("## Check these collections:\n")
        for owner in self.KNOWN_OWNERS:
            results.append(f"- https://skills.sh/{owner}/")
        results.append(f"\n## Direct URL patterns to try:")
        slugs = [
            topic.lower().replace(" ", "-"),
            topic.lower().replace(" ", "_"),
        ]
        for slug in slugs:
            for owner in self.KNOWN_OWNERS[:3]:
                results.append(f"- https://skills.sh/{owner}/skills/{slug}")
        results.append("\n## Also fetch homepage for full leaderboard:")
        results.append("- https://skills.sh")
        return "\n".join(results)

    def _handle_fetch_skill(self, skill_name: str, source: str, owner: str | None) -> str:
        slug = skill_name.lower().strip().replace(" ", "-")

        if source == "skills.sh":
            if owner:
                url = f"https://skills.sh/{owner.rstrip('/')}/{slug}"
            else:
                # Try known owners in order
                results = []
                for o in self.KNOWN_OWNERS:
                    # Try both direct and /skills/ subpath
                    variants = [
                        f"https://skills.sh/{o}/{slug}",
                        f"https://skills.sh/{o}/skills/{slug}",
                    ]
                    for url in variants:
                        content = self._fetch(url)
                        if "❌" not in content[:10]:
                            return content
                        results.append(f"Not found at: {url}")
                return (
                    f"❌ Skill '{slug}' not found in known collections on skills.sh.\n"
                    + "\n".join(results)
                    + "\n\nTry fetch_url with a specific URL."
                )
            return self._fetch(url)

        elif source == "skillhub.club":
            url = f"https://skillhub.club/{slug}"
            return self._fetch(url)

        return f"❌ Unknown source: {source}"

    def _run(self, **kwargs) -> str:
        action = kwargs.get("action")
        url = kwargs.get("url")
        topic = kwargs.get("topic")
        skill_name = kwargs.get("skill_name")
        source = kwargs.get("source", "skills.sh")
        owner = kwargs.get("owner")

        if action == "fetch_url":
            return self._fetch(url or "")
        elif action == "search_skills_sh":
            return self._handle_search_skills_sh(topic or "")
        elif action == "fetch_skill":
            return self._handle_fetch_skill(skill_name or "", source, owner)
        else:
            return f"❌ Unknown action '{action}'. Valid: fetch_url, search_skills_sh, fetch_skill"
