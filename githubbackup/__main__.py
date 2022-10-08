import json
import os.path

import requests
from github import Github

BASE_BACKUP_PATH = "E:\\HDD1Files\\Code\\GitHub Backups"


def backup_repo(repo):
    print(f"\nProcessing repo {repo.name}...")
    latest_commit = repo.get_branch(repo.default_branch).commit.sha

    backup_directory_path = os.path.join(BASE_BACKUP_PATH, repo.name)
    os.makedirs(backup_directory_path, exist_ok=True)

    latest_commit_file_path = os.path.join(backup_directory_path, "latest_commit.txt")
    if os.path.exists(latest_commit_file_path):
        with open(latest_commit_file_path, mode="r") as latest_commit_file:
            last_saved_commit = latest_commit_file.readline().strip()
            if last_saved_commit == latest_commit:
                print("No changes detected. Skipping.")
                return
            else:
                print("Changes detected. Backing up...")

    archive_url = repo.get_archive_link("zipball")
    print(f"Using URL {archive_url}")
    backup_file_path = os.path.join(backup_directory_path, f"{repo.name}.zip")
    with requests.get(archive_url, stream=True, allow_redirects=True) as response:
        response.raise_for_status()
        with open(backup_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    with open(latest_commit_file_path, mode="w") as latest_commit_file:
        latest_commit_file.write(latest_commit)


def backup_repos(github_token: str):
    github = Github(github_token)

    for repo in github.get_user().get_repos():
        backup_repo(repo)


def main():
    with open("credentials.json", mode="r") as credentials_file:
        json_data = json.load(credentials_file)
        github_token = json_data["github_token"]

    backup_repos(github_token)


if __name__ == "__main__":
    main()
