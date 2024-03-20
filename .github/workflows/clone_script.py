import os
import subprocess

# List of repositories to include in the archive
repositories = [
    "https://github.com/rai68/gpsd-easy",
    "https://github.com/rai68/pwnagotchi-pisugar2-plugin/",
    "https://github.com/allordacia/FlipperLink",
    "https://github.com/allordacia/Pwnagotchi-Handshaker",
]

# Directory where the plugins_archive repository is cloned
archive_directory = "../.."  # Navigate up two directories from .github/workflows

def clone_or_update_repository(repo_url, author):
    author_directory = os.path.join(archive_directory, author)
    if not os.path.exists(author_directory):
        os.makedirs(author_directory)
        subprocess.run(["git", "clone", repo_url, author_directory])
    else:
        os.chdir(author_directory)
        subprocess.run(["git", "pull"])

def main():
    # Clone or update repositories
    for repo_url in repositories:
        author = repo_url.split("/")[-2]
        clone_or_update_repository(repo_url, author)

    # Commit and push changes
    os.chdir(archive_directory)
    subprocess.run(["git", "config", "--local", "user.email", "action@github.com"])
    subprocess.run(["git", "config", "--local", "user.name", "GitHub Action"])
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Update archive"])
    subprocess.run(["git", "push"])

if __name__ == "__main__":
    main()
