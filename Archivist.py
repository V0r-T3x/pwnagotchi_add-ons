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
    subprocess.run(["git", "submodule", "add", repo_url, submodule_path], cwd=os.getcwd())  # Set working directory

def remove_submodules():
    # Remove all submodules and author folders except the workflow folder
    for root, dirs, files in os.walk(".", topdown=False):
        for name in dirs:
            if name != ".git" and name != ".github":  # Exclude .git and .github folders
                submodule_path = os.path.join(root, name)
                if os.path.isfile(os.path.join(submodule_path, ".gitmodules")):
                    submodule_rel_path = os.path.relpath(submodule_path, start=os.getcwd())
                    subprocess.run(["git", "submodule", "deinit", "-f", "--", submodule_rel_path], cwd=os.getcwd())  # Set working directory
                    subprocess.run(["git", "rm", "--cached", submodule_rel_path], cwd=os.getcwd())  # Remove from cache, set working directory
                    subprocess.run(["git", "rm", "-rf", submodule_rel_path], cwd=os.getcwd())  # Recursive force remove, set working directory
                    subprocess.run(["git", "config", "--remove-section", f"submodule.{submodule_rel_path}"], cwd=os.getcwd())  # Remove from .gitmodules file, set working directory

    # Remove the parent author folders
    for root, dirs, files in os.walk(".", topdown=True):
        for name in dirs:
            if not any(repo_url.split("/")[-2] == name for repo_url in repositories):
                dir_path = os.path.join(root, name)
                if os.path.isdir(dir_path):
                    subprocess.run(["rm", "-rf", dir_path], cwd=os.getcwd())  # Set working directory

                    
def main():
    # Add repositories as submodules
    for repo_url in repositories:
        add_submodule(repo_url)

    # Initialize and update submodules
    subprocess.run(["git", "submodule", "init"], cwd=os.getcwd())  # Set working directory
    subprocess.run(["git", "submodule", "update"], cwd=os.getcwd())  # Set working directory

    # Remove submodules and author folders
    remove_submodules()

    # Commit and push changes
    subprocess.run(["git", "add", "."], cwd=os.getcwd())  # Set working directory
    subprocess.run(["git", "commit", "-m", "Add and remove submodules"], cwd=os.getcwd())  # Set working directory
    subprocess.run(["git", "push"], cwd=os.getcwd())  # Set working directory

if __name__ == "__main__":
    main()
