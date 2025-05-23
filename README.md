This repo is for subtracting background in JWST MIRI data.


22/05/2025 Managed to sync local folder to git repo.

When pushing code, it always asked me to enter username and password. Here is how I fixed it:
	1. Check for an SSH key (if there isn't one create one): ls ~/.ssh/id_ed25519.pub 
	2. Copy public key via cat ~/.ssh/id_ed25519.pub and create new SSH with it (mine said already in use)
	3. Swith the repo to use SSH: git remote set-url origin <git_repo_SSH starting with git@github.com:>

