import re
import sys
import os


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

print ('''

░░█ █▀ █▀ █▀▀ ▄▀█ █▄░█
█▄█ ▄█ ▄█ █▄▄ █▀█ █░▀█

''')
if len(sys.argv) < 3:
    print("Usage: python regex_search.py <input_dir> <output_file>")
    sys.exit(1)

# Compile the regex patterns
patterns = {k: re.compile(v) for k, v in regex.items()}

# Loop through the files in the input directory and search for the patterns
matches = {}
for root, dirs, files in os.walk(sys.argv[1]):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        for pattern_name, pattern in patterns.items():
            for match in pattern.findall(content):
                if pattern_name not in matches:
                    matches[pattern_name] = []
                matches[pattern_name].append(match)

# Print the matches to the console
for pattern_name, pattern_matches in matches.items():
    print(f'{pattern_name}:')
    for match in pattern_matches:
        print(match)

# Save the matches to the output file
output_file = sys.argv[2]
with open(output_file, 'w') as f:
    for pattern_name, pattern_matches in matches.items():
        f.write(f'{pattern_name}:\n')
        for match in pattern_matches:
            f.write(f'{match}\n')