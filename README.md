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

# Demo
Note that the settings the program asks for are the same as the search filters on https://listingservice.housing.queensu.ca

By default, the program uses no search filters and looks for any new accomodations listed

![image](https://user-images.githubusercontent.com/66915351/210040159-00f3972b-4aa3-4baa-8a9e-95eebfed42b0.png)
![image](https://user-images.githubusercontent.com/66915351/210040234-3fadbe1d-a02a-42bb-8b7a-57780dbb3b18.png)
![image](https://user-images.githubusercontent.com/66915351/210040318-7e9f54bf-bd93-4d05-b6fe-88dd3bbe5086.png)
![image](https://user-images.githubusercontent.com/66915351/210040426-b54c7ef1-131d-45d6-a2dc-50a74231abbd.png)

