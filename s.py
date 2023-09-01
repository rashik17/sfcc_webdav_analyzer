import requests
import json
import csv
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

# Load variables from the .env file into the script's environment
load_dotenv()

base_path = os.getenv("BASE_URL")
base_folder = os.getenv("ROOT_DIR_PATH")
extns = set(os.getenv("EXTENSIONS").split(","))
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_file_size(image_link, access_token):
    response = requests.head(image_link, headers={'Authorization': f'Bearer {access_token}'})

    # Get the size of the image from the Content-Length header
    file_size = int(response.headers.get("Content-Length", 0))
    file_size_kb = file_size / (1024)

    return round(file_size_kb, 2)


#get the access token
def get_access_token():
    url = "https://account.demandware.com/dwsso/oauth2/access_token?grant_type=client_credentials"
    auth = HTTPBasicAuth(client_id, client_secret)
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    access_token = json.loads(requests.request("POST", url, headers=headers, auth=auth).text)['access_token']

    return access_token

# Recursive function to process folders and subfolders
def process_folders(base_path, image_path, access_token, writer):
    response = requests.get(base_path + image_path, headers={'Authorization': f'Bearer {access_token}'})

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)[1:] #skipping first link as it is of parent
        folder_links = []
        for link in links:
            href = link['href']
            if any(href.endswith(ext) for ext in extns):
                size = get_file_size(base_path + href, access_token)
                #print(f"File Extension: {href} with size: {size}")
                writer.writerow([href, size])
            else:
                #print(f"Folders: {href}")
                folder_links.append(href)
        # Recursively process the found folders
        for f_link in folder_links:
            print(f"Processing sub-folder: {f_link}")
            process_folders(base_path, f_link, access_token, writer)
    else:
        print(f"Error: Failed to retrieve images from {image_path}")


# Open the CSV file in write mode
with open(os.getenv("CSV_FILENAME"), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(['File Path', 'Size (KB)'])

    process_folders(base_path, base_folder, get_access_token(), writer)