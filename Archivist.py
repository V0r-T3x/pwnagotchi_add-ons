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
    # Extract the file path from the URL
    file_path = repo_url.split("/blob/main/")[1]

    # Create the folder structure for the file path
    parts = file_path.split("/")
    author = parts[0]
    repo_name = parts[1]
    file_name = parts[2]

    # Create the author folder if it doesn't exist
    if not os.path.exists(author):
        os.makedirs(author)

    # Check if the submodule already exists in the index
    submodule_path = f"{author}/{repo_name}"
    if os.path.exists(submodule_path):
        print(f"Submodule {submodule_path} already exists. Skipping...")
        return

    # Add the file as a submodule within the author folder
    subprocess.run(["git", "submodule", "add", repo_url, file_path], cwd=os.getcwd())  # Set working directory

def remove_submodules():
    # Remove entries from the .gitmodules file and update the index
    for repo_url in repositories:
        file_path = repo_url.split("/blob/main/")[1]
        parts = file_path.split("/")
        author = parts[0]
        repo_name = parts[1]
        submodule_path = os.path.join(author, repo_name)
        subprocess.run(["git", "config", "-f", ".gitmodules", "--remove-section", f"submodule.{submodule_path}"])
        subprocess.run(["git", "rm", "-r", "--cached", submodule_path])

    # Commit the changes to .gitmodules
    subprocess.run(["git", "add", ".gitmodules"])
    subprocess.run(["git", "commit", "-m", "Remove submodule entries from .gitmodules"])

    # Remove the submodule directories
    for repo_url in repositories:
        file_path = repo_url.split("/blob/main/")[1]
        parts = file_path.split("/")
        author = parts[0]
        repo_name = parts[1]
        submodule_path = os.path.join(author, repo_name)
        shutil.rmtree(submodule_path)

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
