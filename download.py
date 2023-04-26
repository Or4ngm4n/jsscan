import sys
import os
import requests
import warnings
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import certifi

print ('''

░░█ █▀ █▀ █▀▀ ▄▀█ █▄░█
█▄█ ▄█ ▄█ █▄▄ █▀█ █░▀█

''')
if len(sys.argv) < 3:
    print("Usage: python download.py <input file name> <output directory>")
    sys.exit(1)

input_file_name = sys.argv[1]
output_dir = sys.argv[2]

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(input_file_name, "r") as f:
    url_list = f.read().splitlines()

for url_str in url_list:
    parsed_url = urlparse(url_str)

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            response = requests.get(url_str, verify=certifi.where())
            soup = BeautifulSoup(response.content, "lxml")

        urls = []
        for script in soup.find_all("script", src=True):
            src = script.get("src")
            if src is not None and src.endswith(".js"):
                parsed_src_url = urlparse(src)
                if parsed_src_url.scheme == "":
                    src = parsed_url.scheme + "://" + parsed_url.netloc + "/" + src.lstrip("/")
                elif parsed_src_url.scheme.startswith("http") and src.startswith("//"):
                    src = parsed_src_url.scheme + ":" + src
                urls.append(src)

        for url in urls:
            response = requests.get(url, verify=certifi.where())
            file_name = url.split("/")[-1]
            with open(output_dir + "/" + file_name, "wb") as f:
                f.write(response.content)
            print("File [+]", file_name, "saved to", output_dir)

    except requests.exceptions.RequestException as e:
        print("Error Can't open this URL [-]:", url_str)
        print(e)
        continue