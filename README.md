#  JsScan
<img src="https://raw.githubusercontent.com/Or4ngm4n/JsScan/main/jsscan.png" width="250" height="70">

Python Scripts to help you discover sensitive data like apikeys, accesstoken, authorizations, jwt,..etc in JavaScript files

# Usage 

```

extract all subdomain into txt file ( urls.txt ) using subfinder and httpx to make sure all subdomain working 
─$ subfinder -d example.com | httpx-toolkit -mc 200 -o urls.txt
─$ cat urls.txt

http://example.com
http://sub1.example.com
http://sub2.example.com
http://sub3.example.com

─$ python extract.py urls.txt js-url.txt
─$ cat js-url.txt
http://example.com/tE8mZYyMFkFuQaS9PqHkE/_buildManifest.js
http://sub1.example.com/static/main.bundle.js
http://sub2.example.com/_next/static/chunks/polyfills-c67a75d1b6f99dc8.js
http://sub3.example.com/static/loadCookieModal.js
─$ python download.py js-url.txt js-directory
─$ ls -al /js-directory
-rw-r--r-- 1 or4ng or4ng 251696 Apr 26 13:40 polyfills-c67a75d1b6f99dc8.js
-rw-r--r-- 1 or4ng or4ng 251696 Apr 26 13:40 _buildManifest.js
-rw-r--r-- 1 or4ng or4ng 251696 Apr 26 13:40 loadCookieModal.js
-rw-r--r-- 1 or4ng or4ng 251696 Apr 26 13:40 main.bundle.js
─$ python jsscan.py js-directory report.txt
─$ cat report.txt
square_access_token:
EAAAAAQAAABoAAAAAAAK.....
twilio_app_sid:
AP7qgh0bgGyz8zcSjCD3mb7hYDmydewdYU....
trello_api_key
0bb5245c839141efbb997cfdc0d21057
```

inspired by <a href="https://github.com/m4ll0k/SecretFinder">@m4ll0k/SecretFinder</a> ❤️
