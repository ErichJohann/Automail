# Automail
This script automatically sends an email to the provided addresses especified on a csv file

### Features:
- OAuth2 authentication with Gmail
- Sends email via Gmail's SMTP server
- Token storage and refresh
- Read the multiple recipients from a CSV file
- Customizable subject and message body from a txt file
- Usage via command line

---

### Requirements
- Google cloud console set up
- Install libraries
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
  - Download de .json and place it on project folder
  - Account used must be added to beta testers for a not published project

### Addresses file 
This file contains all the recipients the email will be send.
- First line --> header
- The following lines each contains an email address on the first column

### Message file
Txt file which provides the content of the email
- First line --> Subject
- Rest --> Body

---

### Running
```bash python Automail.py addresses.csv message.txt```

First use will open a browser window for Google authentication.
Afterward, a token is saved in token.pickle for reuse.

---

### Notes
The first email might be found on email's spam tab
