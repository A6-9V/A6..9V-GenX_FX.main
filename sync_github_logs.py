import datetime
import os
import sys

import requests

# Configuration
USERNAME = os.getenv("GITHUB_USERNAME", "Mouy-leng")
BASE_URL = "https://api.github.com"
OUTPUT_FILE = "UPDATE_LOG.md"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_headers():
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return headers


def get_repos(username):
    url = f"{BASE_URL}/users/{username}/repos"
    repos = []
    page = 1
    headers = get_headers()
    while True:
        try:
            response = requests.get(
                url, params={"page": page, "per_page": 100}, headers=headers, timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if not data:
                    break
                repos.extend(data)
                page += 1
            else:
                print(f"Error fetching repos: {response.status_code} - {response.text}")
                break
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
            break
    return repos


def get_commits(username, repo_name):
    url = f"{BASE_URL}/repos/{username}/{repo_name}/commits"
    headers = get_headers()
    try:
        response = requests.get(
            url, params={"per_page": 10}, headers=headers, timeout=10
        )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 409:  # Empty repository
            return []
        else:
            # Silence error for large number of repos unless it's a major issue
            # print(f"Error fetching commits for {repo_name}: {response.status_code}")
            return []
    except requests.exceptions.RequestException:
        return []


def main():
    print(f"Syncing logs for GitHub account: {USERNAME}")
    repos = get_repos(USERNAME)
    if not repos:
        print("No repositories found or error occurred.")
        return

    print(f"Found {len(repos)} repositories.")

    # Sort repos by last updated
    repos.sort(key=lambda x: x["updated_at"], reverse=True)

    with open(OUTPUT_FILE, "w") as f:
        f.write(f"# Update Log for {USERNAME}\n\n")
        now = datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        )
        f.write(f"Generated on: {now}\n\n")

        for repo in repos:
            repo_name = repo["name"]
            print(f"Fetching logs for {repo_name}...")
            f.write(f"## [{repo_name}]({repo['html_url']})\n")
            if repo["description"]:
                f.write(f"{repo['description']}\n\n")
            else:
                f.write("No description provided.\n\n")

            commits = get_commits(USERNAME, repo_name)
            if not commits:
                f.write("*No commits found (empty repository or error).*\n\n")
            else:
                for commit in commits:
                    sha = commit["sha"][:7]
                    message = commit["commit"]["message"].split("\n")[0]
                    date = commit["commit"]["author"]["date"]
                    f.write(f"- `{sha}`: {message} ({date})\n")
                f.write("\n")

    print(f"Successfully generated {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
