# About

The goal of this quick project is to get email notifications when there is a new listing on https://listingservice.housing.queensu.ca so that my brother who goes to Queen's could find somewhere to live.

# Running the project
```
cd queens-housing-bot
./listing_notifier.sh
```
### or
```
cd queens-housing-bot
# create .env file before running
python main.py
```

### .env format
```
SENDER_ADDRESS="<your email here>"
SENDER_PASSWORD="<your app specific password here>"
```

# Setting up email notifications 
In order to send emails, you will need to provide the app with an email address. I used a GMail account and found that it was required to generate an *App Specific Password* in order to allow the program to send emails on my behalf. Here is a guide for setting it up: https://support.google.com/accounts/answer/185833?hl=en. The email address and *App Specific Password* will need to be set in the .env file. `listing_notifier.sh` will auto create a .env file if there isn't already one and ask for your email and password to set it up.
