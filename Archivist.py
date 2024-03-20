import os
import subprocess

# List of repositories to include in the archive
repositories = [
    "https://github.com/rai68/gpsd-easy",
    "https://github.com/rai68/pwnagotchi-pisugar2-plugin",
    "https://github.com/allordacia/FlipperLink",
    "https://github.com/allordacia/Pwnagotchi-Handshaker",
]

def add_submodule(repo_url):
    # Split the URL to extract the repository name
    repo_name = repo_url.split("/")[-1]

    # Add the repository as a submodule
    subprocess.run(["git", "submodule", "add", repo_url, repo_name])

def main():
    # Add repositories as submodules
    for repo_url in repositories:
        add_submodule(repo_url)

    # Initialize and update submodules
    subprocess.run(["git", "submodule", "init"])
    subprocess.run(["git", "submodule", "update"])

    # Set up git configuration
    subprocess.run(["git", "config", "--local", "user.email", "action@github.com"])
    subprocess.run(["git", "config", "--local", "user.name", "GitHub Action"])
    
    # Set up git credentials
    subprocess.run(["git", "config", "--local", "credential.helper", "store --file=.git/credentials"])
    subprocess.run(["git", "config", "--local", "credential.username", "YOUR_GITHUB_USERNAME"])
    subprocess.run(["git", "config", "--local", "credential.useHttpPath", "true"])

    # Commit and push changes
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Add submodules"])
    subprocess.run(["git", "push"])

if __name__ == "__main__":
    main()
