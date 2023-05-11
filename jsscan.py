import sys
import os
import requests
import warnings
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import certifi
import time

print ('''

░░█ █▀ █▀ █▀▀ ▄▀█ █▄░█
█▄█ ▄█ ▄█ █▄▄ █▀█ █░▀█
      Or4nG.M4n
''')
if len(sys.argv) < 3:
    print("Usage: python extract.py <input file name> <output file name> <output js dir>")
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
    print("Save all .js into directory")
input_js_name = sys.argv[2]
output_dir = sys.argv[3]

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
    print("Try To Find Sinsitive Data ..")

regex = {
    'google_api': r'AIza[0-9A-Za-z-]{35}',
    'google_captcha': r'6L[0-9A-Za-z-]{38}|^6[0-9a-zA-Z-]{39}$',
    'google_oauth': r'ya29.[0-9A-Za-z-]+',
    'firebase': r'AAAA[A-Za-z0-9-]{7}:[A-Za-z0-9_-]{140}',
    'amazon_aws_access_key_id': r'A[SK]IA[0-9A-Z]{16}',
    'amazon_mws_auth_toke': r'amzn\.mws\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
    'amazon_aws_url': r's3.amazonaws.com[/]+|[a-zA-Z0-9_-].s3.amazonaws.com',
    'facebook_access_token': r'EAACEdEose0cBA[0-9A-Za-z]+',
    'authorization_basic': r'basic\s[a-zA-Z0-9=:+/-]+',
    'authorization_bearer': r'bearer\s*[a-zA-Z0-9-.=:+/]+',
    'authorization_api': r'api[key|\s*]+[a-zA-Z0-9-]+',
    'mailgun_api_key': r'key-[0-9a-zA-Z]{32}',
    'twilio_api_key': r'SK[0-9a-fA-F]{32}',
    'twilio_account_sid': r'AC[a-zA-Z0-9_-]{32}',
    'twilio_app_sid': r'AP[a-zA-Z0-9_-]{32}',
    'paypal_braintree_access_token': r'access_token$production$[0-9a-z]{16}$[0-9a-f]{32}',
    'square_oauth_secret': r'sq0csp-[ 0-9A-Za-z-]{43}|sq0[a-z]{3}-[0-9A-Za-z-]{22,43}',
    'square_access_token': r'sqOatp-[0-9A-Za-z-]{22}|EAAA[a-zA-Z0-9]{60}',
    'stripe_standard_api': r'sk_live[0-9a-zA-Z]{24}',
    'stripe_restricted_api': r'rk_live_[0-9a-zA-Z]{24}',
    'github_access_token': r'[a-zA-Z0-9_-]:[a-zA-Z0-9_-]+@github.com',
    'rsa_private_key': r'-----BEGIN RSA PRIVATE KEY-----',
    'ssh_dsa_private_key': r'-----BEGIN DSA PRIVATE KEY-----',
    'ssh_dc_private_key': r'-----BEGIN EC PRIVATE KEY-----',
    'pgp_private_block': r'-----BEGIN PGP PRIVATE KEY BLOCK-----',
    'json_web_token': r'ey[A-Za-z0-9-=]+.[A-Za-z0-9-=]+.?[A-Za-z0-9-_.+/=]*$',
}


patterns = {k: re.compile(v) for k, v in regex.items()}

matches = {}
for root, dirs, files in os.walk(output_dir):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        for pattern_name, pattern in patterns.items():
            for match in pattern.findall(content):
                if pattern_name not in matches:
                    matches[pattern_name] = []
                matches[pattern_name].append(match)

for pattern_name, pattern_matches in matches.items():
    print(f'{pattern_name}:')
    for match in pattern_matches:
        print(match)

output_file = sys.argv[2]
with open(output_file, 'w') as f:
    for pattern_name, pattern_matches in matches.items():
        f.write(f'{pattern_name}:\n')
        for match in pattern_matches:
            f.write(f'{match}\n')
