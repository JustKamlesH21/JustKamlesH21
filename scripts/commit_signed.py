"""Commit files through GitHub's API so the commit is signed by GitHub (shows as Verified)."""
import base64, json, os, subprocess, sys, urllib.request

repo = os.environ["GITHUB_REPOSITORY"]
branch = os.environ.get("BRANCH", "main")
head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
paths = sys.argv[1:]

additions = [{"path": p, "contents": base64.b64encode(open(p, "rb").read()).decode()} for p in paths]
query = """
mutation($input: CreateCommitOnBranchInput!) {
  createCommitOnBranch(input: $input) { commit { oid url } }
}"""
variables = {"input": {
    "branch": {"repositoryNameWithOwner": repo, "branchName": branch},
    "message": {"headline": "chore: refresh stats"},
    "expectedHeadOid": head,
    "fileChanges": {"additions": additions},
}}
req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": query, "variables": variables}).encode(),
    headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
)
res = json.load(urllib.request.urlopen(req))
if "errors" in res:
    raise SystemExit(res["errors"])
print(res["data"]["createCommitOnBranch"]["commit"]["url"])
