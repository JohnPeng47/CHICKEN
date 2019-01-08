This is a small security project that I put together in my spare time, and is inspired by the BEEF browser exploitation framework and XSStrike 
Comprises two parts: 
1) A script to automatically generate a Reflective XSS payload
2) The payload itself which starts reverse shell using a WebSocket client in the injected JS context that communicates back to our listening server. Arbitrary commands can then be sent thru the reverse shell to be executed inside the injected JS context. 

Usage Steps:
1. Install Python3 (Tested with 3.6.6 but will probably work for other versions)
2. Run "npm install"
3. Run "python3 xss.py <website>" to scan for possible Reflective XSS 
4. If the Step 3 is successful, copy the output (it should contain an URL with payload embedded inside a GET parameter) open it in a browser window
5. Start listening server with "node server.js"
6. $$$

Future Features:
1. Filter Evasion
2. More JS modules for the WebSocket client
3. Better commandline interface for the shell (ala Metasploit shell autocomplete, search commands, list modules)


