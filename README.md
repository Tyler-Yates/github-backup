# github-backup
This application makes it easy to back up GitHub repositories locally.

This application will back up every repository the provided token has access to.
The backup will be a zip archive of the repository.
Each user will get their own directory in the backup path.
Underneath each user directory, every repository will get its own subdirectory.

This application will only update the backup if the repository's default branch
has changed.

## Setup
Generate a GitHub token that is able to read the repositories that you want to back up.
Add that token to a file at the root of the repo called `credentials.json`.
This file should be gitignored, so you will need to create this file.
There is an example file you can use for reference:
```bash
cp credentials.json.example credentials.json
```

## Running
After setting up your virtual environment and installing the requirements, you can run
the back-up with the following command:
```bash
python3 -m githubbackup
```
