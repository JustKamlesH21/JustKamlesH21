"""Pull public GitHub stats into data/stats.json (run by .github/workflows/stats.yml)."""
import datetime as dt, json, os, urllib.request

LOGIN = os.environ.get("GH_LOGIN", "JustKamlesH21")
TOKEN = os.environ["GITHUB_TOKEN"]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false, first: 100) {
      totalCount
      nodes { stargazerCount languages(first: 20) { edges { size node { name } } } }
    }
  }
}"""

req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
    headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
)
res = json.load(urllib.request.urlopen(req))
if "errors" in res:
    raise SystemExit(res["errors"])
u = res["data"]["user"]
cal = u["contributionsCollection"]["contributionCalendar"]
langs = {}
for repo in u["repositories"]["nodes"]:
    for e in repo["languages"]["edges"]:
        langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]

data = {
    "login": LOGIN,
    "total": cal["totalContributions"],
    "calendar": [[d["date"], d["contributionCount"]] for w in cal["weeks"] for d in w["contributionDays"]],
    "repos": u["repositories"]["totalCount"],
    "stars": sum(r["stargazerCount"] for r in u["repositories"]["nodes"]),
    "followers": u["followers"]["totalCount"],
    "langs": langs,
    "updated": dt.date.today().isoformat(),
}
os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
json.dump(data, open(os.path.join(ROOT, "data", "stats.json"), "w"))
print(f"{data['total']} contributions, {data['repos']} repos")
