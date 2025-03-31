# Automail
This script automatically sends an email to the provided addresses specified on a csv file

### Features:
- OAuth2 authentication with Gmail
- Sends email via Gmail's SMTP server
- Token storage and refresh
- Reads the multiple recipients from a CSV file
- Customizable subject and message body from a txt file
- Usage via command line

---

### Requirements
- Google cloud console set up
- Install required libraries
  - google-auth
  - google-auth-oauthlib
  - google-api-python-client

 ### Google cloud
   - Go to https://console.cloud.google.com/
   - Create a new project
   - Activate gmail api
   - Necessary scopes:
     - googleapis.com/auth/gmail.readonly
     - mail.google.com
     - googleapis.com/auth/gmail.send
  - Create OAuth 2.0 Client ID credentials
  - Download the .json and place it in the project folder
  - Account used must be added as a beta tester for unpublished projects

### Addresses file 
This file contains all the recipients the email will be sent
- First line --> header
- The following lines each contains an email address on the first column

### Message file
A txt file that provides the email content
- First line --> Subject
- Rest --> Body

---

### Running
```bash python Automail.py addresses.csv message.txt```

First use will open a browser window for Google authentication.
Afterward, a token is saved in token.pickle for reuse.

---

### Notes
The first email might be found in the spam folder
