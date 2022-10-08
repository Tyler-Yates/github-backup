import json
import os.path

import requests
from github import Github


def backup_repo(repo, user_login: str, backup_path: str):
    print(f"\nProcessing repo {repo.name}...")
    latest_commit = repo.get_branch(repo.default_branch).commit.sha

    backup_directory_path = os.path.join(backup_path, user_login, repo.name)
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


def backup_repos(github_token: str, backup_path: str):
    github = Github(github_token)

    user = github.get_user()

    print("\n==============================================================================================")
    print(f"Backing up repos for user {user.name!r} ({user.login})")

    for repo in user.get_repos():
        backup_repo(repo=repo, user_login=user.login, backup_path=backup_path)


def main():
    with open("credentials.json", mode="r") as credentials_file:
        json_data = json.load(credentials_file)
        github_tokens = json_data["github_tokens"]
        backup_path = json_data["backup_path"]

    for github_token in github_tokens:
        backup_repos(github_token=github_token, backup_path=backup_path)


if __name__ == "__main__":
    main()
