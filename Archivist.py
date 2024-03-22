import os
import subprocess
import shutil

# List of repositories to include in the archive
repositories = [
    "https://github.com/LegendEvent/pwnagotchi-custom-plugins/blob/main/achievements.py",
    "https://github.com/AlienMajik/pwnagotchi_plugins/blob/main/adsbsniffer.py",
    "https://github.com/Sniffleupagus/pwnagotchi_plugins/blob/main/enable_assoc.py",
    "https://github.com/Sniffleupagus/pwnagotchi_plugins/blob/main/enable_deauth.py",
]

def add_submodule(repo_url):
    # Split the URL to extract the repository owner, name, and branch
    parts = repo_url.split("/")
    if len(parts) < 5:
        print(f"Invalid URL format: {repo_url}")
        return

    # Extract the repository owner, name, and branch
    owner = parts[3]
    repo_name = parts[4]
    branch = "main"  # Assuming the default branch is 'main'

    # Create the author folder if it doesn't exist
    author_folder = os.path.join(owner)
    if not os.path.exists(author_folder):
        os.makedirs(author_folder)

    # Check if the submodule already exists in the index
    submodule_path = os.path.join(author_folder, repo_name)
    if os.path.exists(submodule_path):
        print(f"Submodule {submodule_path} already exists. Skipping...")
        return

    # Construct the clone URL
    clone_url = f"https://github.com/{owner}/{repo_name}.git"
    
    # Add the repository as a submodule within the author folder
    subprocess.run(["git", "submodule", "add", "--branch", branch, clone_url, submodule_path], cwd=os.getcwd())  # Set working directory



def remove_submodules():
    # Remove entries from the .gitmodules file and update the index
    for repo_url in repositories:
        parts = repo_url.split("/")
        author = parts[3]
        repo_name = parts[4].split(".git")[0]
        submodule_path = os.path.join(author, repo_name)
        subprocess.run(["git", "config", "-f", ".gitmodules", "--remove-section", f"submodule.{submodule_path}"])
        subprocess.run(["git", "rm", "-r", "--cached", submodule_path])

    # Commit the changes to .gitmodules
    try:
        subprocess.run(["git", "add", ".gitmodules"])
        subprocess.run(["git", "commit", "-m", "Remove submodule entries from .gitmodules"])
    except subprocess.CalledProcessError:
        pass

    # Remove the submodule directories
    for repo_url in repositories:
        parts = repo_url.split("/")
        author = parts[3]
        repo_name = parts[4].split(".git")[0]
        submodule_path = os.path.join("_plugins_archive", author, repo_name)
        try:
            shutil.rmtree(submodule_path)
        except FileNotFoundError:
            pass

    # Commit the changes
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Remove submodules"])



    # Remove the parent author folders
    #for root, dirs, files in os.walk(".", topdown=True):
    #    for name in dirs:
    #        if not any(repo_url.split("/")[-2] == name for repo_url in repositories):
    #            dir_path = os.path.join(root, name)
    #            if os.path.isdir(dir_path):
    #                shutil.rmtree(dir_path)


                    
def main():
    subprocess.run(["git", "config", "--global", "user.email", "70115207+V0r-T3x@users.noreply.github.com"])
    subprocess.run(["git", "config", "--global", "user.name", "V0r-T3x"])
    
    # Add repositories as submodules
    for repo_url in repositories:
        add_submodule(repo_url)

    # Initialize and update submodules
    subprocess.run(["git", "submodule", "init"], cwd=os.getcwd())  # Set working directory
    subprocess.run(["git", "submodule", "update"], cwd=os.getcwd())  # Set working directory

    # Remove submodules and author folders
    #remove_submodules()

    # Commit and push changes
    subprocess.run(["git", "add", "."], cwd=os.getcwd())  # Set working directory
    subprocess.run(["git", "commit", "-m", "Add and remove submodules"], cwd=os.getcwd())  # Set working directory
    subprocess.run(["git", "push"], cwd=os.getcwd())  # Set working directory

if __name__ == "__main__":
    main()
