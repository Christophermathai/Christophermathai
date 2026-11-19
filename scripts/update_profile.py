#!/usr/bin/env python3
"""Refresh the profile SVG with public GitHub account statistics."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "assets" / "profile-stats.svg"
USERNAME = os.environ.get("GITHUB_USERNAME", "Christophermathai")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
API = "https://api.github.com"


def api_get(path: str):
    url = API + path
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ChristopherMathai-Profile-Stats",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API returned HTTP {exc.code} for {path}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach GitHub API: {exc.reason}") from exc


def get_public_repositories(username: str):
    repositories = []
    page = 1
    while True:
        query = urllib.parse.urlencode({"type": "owner", "per_page": 100, "page": page})
        batch = api_get(f"/users/{urllib.parse.quote(username)}/repos?{query}")
        if not isinstance(batch, list):
            raise RuntimeError("Unexpected response while listing repositories")
        repositories.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repositories


def format_number(value: int) -> str:
    return f"{value:,}"


def main() -> int:
    profile = api_get(f"/users/{urllib.parse.quote(USERNAME)}")
    repositories = get_public_repositories(USERNAME)

    # The user endpoint is the source of truth for the public repository count.
    stats = {
        "repos": int(profile.get("public_repos", len(repositories))),
        "stars": sum(int(repo.get("stargazers_count", 0)) for repo in repositories),
        "followers": int(profile.get("followers", 0)),
        "forks": sum(int(repo.get("forks_count", 0)) for repo in repositories),
    }

    tree = ET.parse(ASSET)
    root = tree.getroot()
    ns = "{http://www.w3.org/2000/svg}"
    for key, value in stats.items():
        element = root.find(f".//*[@id='{key}']")
        if element is None:
            raise RuntimeError(f"Missing SVG element id={key}")
        element.text = format_number(value)

    updated = root.find(f".//*[@id='updated']")
    if updated is not None:
        updated.text = "Updated " + datetime.now(timezone.utc).strftime("%d %b %Y")

    ET.register_namespace("", "http://www.w3.org/2000/svg")
    tree.write(ASSET, encoding="utf-8", xml_declaration=True)
    print("Updated profile statistics:", stats)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:  # keep CI failure message visible
        print(f"Profile statistics update failed: {error}", file=sys.stderr)
        raise
