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
    # Split the URL to extract the repository owner and name
    parts = repo_url.strip("/").split("/")
    author = parts[-2]
    repo_name = parts[-1]

    # Create the author folder if it doesn't exist
    if not os.path.exists(author):
        os.makedirs(author)

    # Check if the submodule already exists in the index
    submodule_path = f"{author}/{repo_name}"
    if os.path.exists(submodule_path):
        print(f"Submodule {submodule_path} already exists. Skipping...")
        return

    # Add the repository as a submodule within the author folder
    subprocess.run(["git", "submodule", "add", repo_url, submodule_path])

def remove_submodules():
    # Remove all submodules and author folders except the workflow folder
    for root, dirs, files in os.walk(".", topdown=False):
        for name in dirs:
            if name != ".git" and name != ".github":  # Exclude .git and .github folders
                submodule_path = os.path.join(root, name)
                if os.path.isfile(os.path.join(submodule_path, ".gitmodules")):
                    subprocess.run(["git", "submodule", "deinit", "-f", "--", submodule_path])
                    subprocess.run(["git", "rm", "-rf", submodule_path])  # Recursive force remove
                    subprocess.run(["git", "config", "--remove-section", f"submodule.{submodule_path}"])

    # Remove the parent author folders
    for repo_url in repositories:
        author = repo_url.split("/")[-2]
        if os.path.exists(author):
            subprocess.run(["rm", "-rf", author])

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

    # Commit and push changes
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Add submodules"])
    subprocess.run(["git", "push"])

    # Remove submodules and author folders
    remove_submodules()

if __name__ == "__main__":
    main()
