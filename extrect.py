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
    print("Usage: python extract.py <input file name> <output file name>")
    sys.exit(1)

input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

# Read the input URLs from the file
with open(input_file_name, "r") as f:
    url_list = f.read().splitlines()

with open(output_file_name, "w") as f_out:
    for url_str in url_list:
        parsed_url = urlparse(url_str)

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=UserWarning)
                response = requests.get(url_str, verify=certifi.where())
                soup = BeautifulSoup(response.content, "html.parser")

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
                f_out.write(url + "\n")
                print("URL [+]", url, "saved to", output_file_name)

        except requests.exceptions.RequestException as e:
            print("Error Can't open this URL:", url_str)
            print(e)
            continue