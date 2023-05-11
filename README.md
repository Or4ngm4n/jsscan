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

─$ python jsscan.py urls.txt js-url.txt js-directory

░░█ █▀ █▀ █▀▀ ▄▀█ █▄░█
█▄█ ▄█ ▄█ █▄▄ █▀█ █░▀█

URL [+] http://example.com/tE8mZYyMFkFuQaS9PqHkE/_buildManifest.js saved to js-url.txt
URL [+] http://sub1.example.com/static/main.bundle.js saved to js-url.txt
URL [+] http://sub2.example.com/_next/static/chunks/polyfills-c67a75d1b6f99dc8.js saved to js-url.txt
URL [+] http://sub3.example.com/static/loadCookieModal.js saved to js-url.txt
Save all .js into directory
File [+] http://example.com/tE8mZYyMFkFuQaS9PqHkE/_buildManifest.js
File [+] http://sub1.example.com/static/main.bundle.js
File [+] http://sub2.example.com/_next/static/chunks/polyfills-c67a75d1b6f99dc8.js
File [+] http://sub3.example.com/static/loadCookieModal.js
Trying To Find Sinsitive Data ..
google_captcha:
6Ly93d3cudzMub3JnLzI.....
6Ly93d3cudzMub3JnLzI.....
square_access_token:
EAAAAAQAAABoAAAAAAAK.....
twilio_app_sid:
AP7qgh0bgGyz8zcSjCD3mb7hYDmydewdYU....
trello_api_key
0bb5245c839141efbb997cfdc0d21057
result Name :result.txt
cat result.txt
google_captcha:
6Ly93d3cudzMub3JnLzI.....
6Ly93d3cudzMub3JnLzI.....
square_access_token:
EAAAAAQAAABoAAAAAAAK.....
twilio_app_sid:
AP7qgh0bgGyz8zcSjCD3mb7hYDmydewdYU....
trello_api_key
0bb5245c839141efbb997cfdc0d21057
```
Thnaks For Help\Update this tool <a href="https://github.com/az7rb">@az7rb</a> ❤️
inspired by <a href="https://github.com/m4ll0k/SecretFinder">@m4ll0k/SecretFinder</a> ❤️
