import os
import subprocess
import shutil
import requests
import toml

# Get the path to the codex.toml file
script_dir = os.path.dirname(os.path.abspath(__file__))
codex_path = os.path.join(script_dir, "codex.toml")

# Load the contents of codex.toml
with open(codex_path, "r") as file:
    codex_data = toml.load(file)

# Access the sections and their lists
plugins_list = codex_data["plugins"]["list"]
scripts_list = codex_data["scripts"]["list"]
mods_list = codex_data["mods"]["list"]
apps_list = codex_data["apps"]["list"]

# Function to get the last commit date of a file in a repository
def get_last_commit_date(repo_url):
    parts = repo_url.split("/")
    owner = parts[3]
    repo_name = parts[4].split(".git")[0]
    branch = "main"  # Assuming the default branch is 'main'
    
    api_url = f"https://api.github.com/repos/{owner}/{repo_name}/commits/{branch}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        commit_data = response.json()
        last_commit_date = commit_data["commit"]["author"]["date"]
        return last_commit_date
    except requests.RequestException as e:
        print(f"Error fetching last commit date for {repo_url}: {e}")
        return None

def add_submodule(file_path, folder_name):

    parts = file_path.split("/")
    owner = parts[3]
    repo_name = parts[4].split(".git")[0]
    branch = "main"  # Assuming the default branch is 'main'
    last_commit_date = get_last_commit_date(file_path)
    description = None

    # Create the author folder if it doesn't exist
    author_folder = os.path.join(folder_name, owner)

    if file_path.endswith(('.py', '.txt', '.json', '.csv')):  # If it's a file URL
        file_relative_path = "/".join(parts[5:])
        file_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/{branch}/{file_relative_path}"

        if file_url.endswith(".py"):
            response = requests.get(file_url)
            if response.status_code == 200:
                lines = response.text.split("\n")
                for line in lines:
                    if "__description__" in line:
                        description = line.split("__description__")[1].strip()
                        break
    else:  # If it's a repository URL
        if not os.path.exists(author_folder):
            os.makedirs(author_folder)

    # Check if the submodule already exists in the index
    submodule_path = os.path.join(author_folder, repo_name)
    if os.path.exists(submodule_path):
        print(f"Submodule {submodule_path} already exists. Skipping...")
        return {
            "owner": owner,
            "repo_name": repo_name,
            "branch": branch,
            "last_commit_date": last_commit_date,
            "file_relative_path": None,
            "description": None
        }

    # Construct the clone URL
    clone_url = f"https://github.com/{owner}/{repo_name}.git"
    
    # Add the repository as a submodule within the author folder
    subprocess.run(["git", "submodule", "add", "--branch", branch, clone_url, submodule_path], cwd=os.getcwd())  # Set working directory

    return {
        "owner": owner,
        "repo_name": repo_name,
        "branch": branch,
        "last_commit_date": last_commit_date,
        "file_relative_path": file_relative_path if file_path.endswith(('.py', '.txt', '.json', '.csv')) else None,
        "description": description
    }


def remove_submodules(submodules_list, folder_name):
    # Remove entries from the .gitmodules file and update the index
    for submodule_url in submodules_list:
        parts = submodule_url.split("/")
        author = parts[3]
        repo_name = parts[4].split(".git")[0]
        submodule_path = os.path.join("Plugins", author, repo_name)
        subprocess.run(["git", "config", "-f", ".gitmodules", "--remove-section", f"submodule.{submodule_path}"])
        #subprocess.run(["git", "rm", "-r", "--cached", submodule_path])

    # Stage changes to .gitmodules
    subprocess.run(["git", "add", ".gitmodules"])

    # Commit the changes to .gitmodules
    subprocess.run(["git", "commit", "-m", "Remove submodule entries from .gitmodules"])

    # Remove the submodule directories
    for submodule_url in submodules_list:
        parts = submodule_url.split("/")
        author = parts[3]
        repo_name = parts[4].split(".git")[0]
        submodule_path = os.path.join(folder_name, author, repo_name)
        if os.path.exists(submodule_path):
            try:
                shutil.rmtree(submodule_path)
            except FileNotFoundError:
                pass
        else:
            print(f"Submodule {submodule_path} does not exist. Skipping deletion...")


    # Commit the changes
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Remove submodules"])


def main():
    subprocess.run(["git", "config", "--global", "user.email", "70115207+V0r-T3x@users.noreply.github.com"])
    subprocess.run(["git", "config", "--global", "user.name", "V0r-T3x"])
    
    # Add plugin repositories as submodules
    #for plugin_url in plugins_list:
    #    submodule_info = add_submodule(plugin_url, "Plugins")
    #    print(submodule_info)

    #for mods_url in mods_list:
    #    submodule_info = add_submodule(mods_url, "Mods")
    #    print(submodule_info)

    # Initialize and update submodules
    subprocess.run(["git", "submodule", "init"], cwd=os.getcwd())  # Set working directory
    subprocess.run(["git", "submodule", "update"], cwd=os.getcwd())  # Set working directory

    # Remove plugins submodules and author folders
    #remove_submodules(plugins_list, "Plugins")

    # Remove mods submodules and author folders
    remove_submodules(mods_list, "Mods")

    # Commit and push changes
    subprocess.run(["git", "add", "."], cwd=os.getcwd())  # Set working directory
    subprocess.run(["git", "commit", "-m", "Add and remove submodules"], cwd=os.getcwd())  # Set working directory
    subprocess.run(["git", "push"], cwd=os.getcwd())  # Set working directory

if __name__ == "__main__":
    main()
