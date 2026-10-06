import json
import os
import requests
from collections import Counter

USERNAME = os.environ.get("GH_PROFILE_USER", "SAIRAJA-2K7")
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "profile_stats.json")

S = requests.Session()
S.headers.update({
    "Accept": "application/vnd.github+json",
    "User-Agent": "github-profile-readme"
})

def get(url, params=None):
    r = S.get(url, params=params, timeout=20)
    r.raise_for_status()
    return r.json()

user = get(f"https://api.github.com/users/{USERNAME}")

repos = []
page = 1

while True:
    batch = get(
        f"https://api.github.com/users/{USERNAME}/repos",
        {"per_page": 100, "page": page, "type": "owner"}
    )
    if not batch:
        break
    repos.extend(batch)
    if len(batch) < 100:
        break
    page += 1

stars = sum(r.get("stargazers_count", 0) for r in repos)
forks = sum(r.get("forks_count", 0) for r in repos)

languages = Counter()

for repo in repos:
    try:
        langs = get(repo["languages_url"])
        for language, amount in langs.items():
            languages[language] += amount
    except requests.RequestException:
        pass

# GitHub Search API gives public PR/issue counts authored by the user.
prs = get(
    "https://api.github.com/search/issues",
    {"q": f"is:pr author:{USERNAME}", "per_page": 1}
)["total_count"]

issues = get(
    "https://api.github.com/search/issues",
    {"q": f"is:issue author:{USERNAME}", "per_page": 1}
)["total_count"]

profile = {
    "username": USERNAME,
    "name": user.get("name") or USERNAME,
    "bio": user.get("bio") or "",
    "public_repos": user.get("public_repos", 0),
    "followers": user.get("followers", 0),
    "following": user.get("following", 0),
    "stars": stars,
    "forks": forks,
    "pull_requests": prs,
    "issues": issues,
    "top_languages": [
        {"name": name, "bytes": count}
        for name, count in languages.most_common(8)
    ],
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(profile, f, indent=2)

print(f"wrote {OUT}")
print(f"repositories: {profile['public_repos']}")
print(f"stars: {profile['stars']}")
print(f"forks: {profile['forks']}")
print(f"pull requests: {profile['pull_requests']}")
print(f"issues: {profile['issues']}")
print("languages:", ", ".join(x["name"] for x in profile["top_languages"]))
