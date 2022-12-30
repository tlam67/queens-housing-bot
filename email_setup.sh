echo "Creating .env file..."
echo "Enter email address to send notifications FROM:"
read email
echo "App Specific Password guide: https://support.google.com/accounts/answer/185833?hl=en"
echo "Enter App Specific Passsword for that email:"
read pass
echo "SENDER_ADDRESS=\"$email\"" >> .env
echo "SENDER_PASSWORD=\"$pass\"" >> .env