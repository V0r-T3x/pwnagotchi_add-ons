import os
import subprocess

# List of repositories to include in the archive
repositories = [
    "https://github.com/rai68/gpsd-easy",
    "https://github.com/rai68/pwnagotchi-pisugar2-plugin",
    "https://github.com/allordacia/FlipperLink",
    "https://github.com/allordacia/Pwnagotchi-Handshaker",
]

def clone_or_update_repository(repo_url):
    # Split the URL to extract the repository owner and name
    parts = repo_url.strip("/").split("/")
    if len(parts) == 5:  # If the URL contains both owner and repo name
        author = parts[-2]
        repo_name = parts[-1]
    else:  # If the URL contains only the repo name
        author = ""
        repo_name = parts[-1]

    print("Author:", author)
    print("Repository:", repo_name)
    print("URL:", repo_url)
    author_directory = os.path.join(author, repo_name)
    if not os.path.exists(author_directory):
        print(author_directory)
        os.makedirs(author_directory)
        subprocess.run(["git", "clone", repo_url, author_directory])
    else:
        os.chdir(author_directory)
        subprocess.run(["git", "pull"])

def main():
    # Clone or update repositories
    print("Hack The Planet")
    #print(os.path)
    for repo_url in repositories:
        #author, repo_name = repo_url.split("/")[-2:]
        clone_or_update_repository(repo_url)
    # Commit and push changes
    #subprocess.run(["git", "config", "--local", "user.email", "action@github.com"])
    #subprocess.run(["git", "config", "--local", "user.name", "GitHub Action"])
    #subprocess.run(["git", "add", "."])
    #subprocess.run(["git", "commit", "-m", "Update archive"])
    #subprocess.run(["git", "push"])

if __name__ == "__main__":
    main()
