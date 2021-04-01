# References and links: 
# How to get the pull request number? 
# https://stackoverflow.com/questions/59077079/how-to-get-pull-request-number-within-github-actions-workflow
# How to know the pull request branches involved?
# https://stackoverflow.com/questions/15096331/github-api-how-to-find-the-branches-of-a-pull-request

import base64
import json
import sys
import os

# This script checks the pull request files
# It will succeed only if the pull request has the following characteristics:
# - It comes from a branch different from main/master
# - It only changes one file, located at balls/ and with extention .txt
# - The file only has 1 char

# We create an auxiliar function to download jsons
def download_json(api_url, my_token, json_file, debug=False):
    """
    """
    order = f'curl --header "authorization: Bearer {my_token}" \
              -H "Accept: application/vnd.github.v3+json" \
              {api_url} \
              -o {json_file}'
    if debug: 
        print(order)
    else:
        order += '> debug_file.txt 2>&1'

    os.system(order)
    return

# Config - Most likely this will be dynamic parameters
if len(sys.argv)==5:
    # Use it as in:
    #   python check_pull_request.py PR_NUMBER ${{ secrets.GITHUB_TOKEN }} $GITHUB_USER $GITHUB_REPOSITORY 
    REPO = sys.argv[1]
    PR_NUMBER = sys.argv[2]
    TOKEN = sys.argv[3]
else:
    REPO = "sebastiandres/pull_request_training_repo"
    PR_NUMBER = 1 # This will change
    TOKEN = "" #Personal Access Token

################################################################################
# Checking the branch
################################################################################
PR_url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}"
PR_json = "Step_0_PR_info.json"
download_json(PR_url, TOKEN, PR_json)

with open(PR_json) as json_file:
    json_dict = json.load(json_file)
    # Get the origin of the PR  
    PR_user, PR_branch = json_dict["head"]["label"].split(":")
    # Get where the PR is trying to write
    base_user, base_branch = json_dict["base"]["label"].split(":")
    print("From: ", PR_user, PR_branch)
    print("To: ", base_user, base_branch)
    # If the pull request comes from the same user, dont check.
    # We'll asume he's knowing what to do. 
    # So we stop and send a clean exit (0) 
    if PR_user == base_user:
        sys.exit(0)
    # Stop if needed
    print("\n ELIMINATE THIS AFTER TESTING \n")
    if False:
      if PR_branch in ["main", "master"]:
          raise Exception("Pull Request must come from a branch, not from main/master.")

################################################################################
# Checking the number of files
################################################################################
PR_files_json = "Step_1_PR_files.json"
PR_files_url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files"
download_json(PR_files_url, TOKEN, PR_files_json)

with open(PR_files_json) as json_file:
    # Load the files
    data = json.load(json_file)
    # Select the files, so we can print them if more than one
    if len(data)==0 or "filename" not in data[0]:
      print("Hmm, something unexpected. Printing the received file")
      print(data)
      raise Exception("Unexpected PR file structure.")
    # Print all the files in the PR
    all_PR_files = [data[i]["filename"] for i in range(len(data))]
    print(f"{len(all_PR_files)} Files in PR: {', '.join(all_PR_files)}")
    # Count the files
    if not len(data)==1:
      raise Exception("More than 1 file.")
    else:
      PR_filename = data[0]["filename"]
    if not PR_filename.startswith("balls/"):
      raise Exception("Not in correct folder.")
    if not PR_filename.endswith(".txt"):
      raise Exception("Not the expected extension.")
    # Get the file url to download it (now we know it's only one)
    PR_content_url = data[0]["contents_url"] 

################################################################################
# Checking the content of the file
################################################################################
# PR_content_url defined above while looking at files
PR_content_json = "Step_2_PR_content.json"
download_json(PR_content_url, TOKEN, PR_content_json)

with open(PR_content_json) as json_file:
    # Load the files
    data = json.load(json_file)
    content = data["content"]
    encoding = data["encoding"]
    if encoding=="base64":
        decoded_content = base64.b64decode(bytes(content, 'utf-8'))
        true_content = decoded_content.strip()
    else:
        true_content = content.decode("utf8").strip()
    if len(true_content)!=1:
      raise Exception("New file has more than one char.")

# If we arrive here, everything is OK
print("All good on the PR")