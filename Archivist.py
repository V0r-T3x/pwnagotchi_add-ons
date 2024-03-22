import os
import subprocess
import shutil
import requests

# List of plugins to include in the archive
plugin_list = [
    "https://github.com/LegendEvent/pwnagotchi-custom-plugins/blob/main/achievements.py",
    "https://github.com/AlienMajik/pwnagotchi_plugins/blob/main/adsbsniffer.py",
    "https://github.com/Sniffleupagus/pwnagotchi_plugins/blob/main/enable_assoc.py",
    "https://github.com/Sniffleupagus/pwnagotchi_plugins/blob/main/enable_deauth.py",
]

# Function to get the last commit date of a file in a repository
def get_last_commit_date(repo_url):
    api_url = repo_url.replace("github.com", "api.github.com/repos").replace("blob/main", "commits/main")  # Convert URL to GitHub API URL
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()["commit"]["commit"]["author"]["date"]
    else:
        print(f"Error: Unable to fetch commit date for {repo_url}")
        return None

def add_submodule(file_path):
    if "github.com" in file_path:  # If it's a file URL
        parts = file_path.split("/")
        owner = parts[3]
        repo_name = parts[4]
        branch = "main"
        file_relative_path = "/".join(parts[5:])
        file_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/{branch}/{file_relative_path}"
        last_commit_date = get_last_commit_date(file_path)
        description = None
        if file_url.endswith(".py"):
            response = requests.get(file_url)
            if response.status_code == 200:
                lines = response.text.split("\n")
                for line in lines:
                    if "_description_" in line:
                        description = line.split("_description_")[1].strip()
                        break
        return {
            "owner": owner,
            "repo_name": repo_name,
            "branch": branch,
            "last_commit_date": last_commit_date,
            "file_relative_path": file_relative_path,
            "description": description
        }
    else:  # If it's a repository URL
        parts = file_path.split("/")
        owner = parts[3]
        repo_name = parts[4].split(".git")[0]
        branch = "main"  # Assuming the default branch is 'main'
        last_commit_date = get_last_commit_date(file_path)
        return {
            "owner": owner,
            "repo_name": repo_name,
            "branch": branch,
            "last_commit_date": last_commit_date,
            "file_relative_path": None,
            "description": None
        }

def remove_submodules():
    # Remove entries from the .gitmodules file and update the index
    for file_url in plugin_list:
        parts = file_url.split("/")
        author = parts[3]
        repo_name = parts[4].split(".git")[0]
        submodule_path = os.path.join("Plugins", author, repo_name)
        subprocess.run(["git", "config", "-f", ".gitmodules", "--remove-section", f"submodule.{submodule_path}"])
        subprocess.run(["git", "rm", "-r", "--cached", submodule_path])

    # Stage changes to .gitmodules
    subprocess.run(["git", "add", ".gitmodules"])

    # Commit the changes to .gitmodules
    subprocess.run(["git", "commit", "-m", "Remove submodule entries from .gitmodules"])

    # Remove the submodule directories
    for file_url in plugin_list:
        parts = file_url.split("/")
        author = parts[3]
        repo_name = parts[4].split(".git")[0]
        submodule_path = os.path.join("Plugins", author, repo_name)
        try:
            shutil.rmtree(submodule_path)
        except FileNotFoundError:
            pass

    # Commit the changes
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Remove submodules"])


def main():
    subprocess.run(["git", "config", "--global", "user.email", "70115207+V0r-T3x@users.noreply.github.com"])
    subprocess.run(["git", "config", "--global", "user.name", "V0r-T3x"])
    
    # Add plugin repositories as submodules
    #for plugin_url in plugin_list:
    #    submodule_info = add_submodule(plugin_url)
    #    print(submodule_info)

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
