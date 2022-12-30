import requests
from bs4 import BeautifulSoup
import datetime as dt
from threading import Thread, Event
import keyboard
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
import re

load_dotenv()
SENDER_ADDRESS=os.getenv('SENDER_ADDRESS')
SENDER_PASSWORD=os.getenv('SENDER_PASSWORD')

email_validator = re.compile('[^@]+@[^@]+\.[^@]+')

class Listing:
  def __init__(self, info) -> None:
    self.img = None
    self.address = None
    self.type = None
    self.lease_type = None
    self.rooms = None
    self.available = None
    self.lease_start = None
    self.rent = None
    self.contact = None
    self.details = None
    self.parse(info)

  def parse(self, parsed_row):
    data = parsed_row.find_all('td')
    if len(data) != 10:
      print("not length 10, unknown format")
      return
    
    self.img = parsed_row.img['src']
    self.address = data[1].text
    self.type = data[2].text
    self.lease_type = data[3].text
    self.rooms = data[4].text
    self.available = data[5].text
    self.lease_start = data[6].text
    self.rent = data[7].text
    self.contact = data[8].text
    self.details = data[9].a['href']

  def display(self):
    info = vars(self)
    for key in info:
      print(f'{key:<15} {info[key]}')

  def getContent(self):
    content = f'<h1>{self.address}</h1>'
    content += f'<img width="400" src="{self.img}">'
    content += f'<table style="border-spacing: 30px 0;">'
    data = vars(self)
    for key in data:
      if key == "img": continue
      content += "<tr><td>" + key.replace('_', ' ') + "</td>" + "<td>" + data[key] + "</td></tr>"

    content += f'</table>'
    return content

class ListingManager:
  BASE_API_URL = "https://listingservice.housing.queensu.ca/public/getByFilter?"
  DATE = "DATE"
  BOOL = "BOOL"
  STRING = "STRING"
  INT = "INT"

  def __init__(self) -> None:
    self.listings = {}
    self.email = None
    self.property_type_id = None
    self.lease_type_id = None
    self.number_of_rooms = None
    self.shared_accommodation = False
    self.water_included = False
    self.heat_included = False
    self.electricity_included = False
    self.furnished = False
    self.parking_available = False
    self.air_conditioning = False
    self.accessibility_features = False
    self.laundry_hookup = False
    self.onsite_laundry = False
    self.landlord_contract_program = False
    self.queens_owned = False
    self.date_available = dt.date.today()
    self.show_test = 0
    self.num_items = "all"
    self.frequency = 60
    self.active = False
    self.timer = Event()
    self.test = False
    self.configure()
    self.current_settings()

  def getInput(self, options, type):
    print()       # print new line for spacing
    display = ''
    inp = None
    if type == self.STRING:
      for i, option in enumerate(options):
        if i != 0:
          display +=  ', '
        display += f'{i + 1}: {option}'
      while not isinstance(inp, int) or inp > len(options) or inp < 1:
        inp = input(display + "\nChoose an option (input nothing for default): ")
        try:
          if inp == "":
            inp = 0
            break
          inp = int(inp)
        except ValueError:
          print("Input must be an integer")
      inp = options[inp]
    elif type == self.BOOL:
      for option in options:
        display += option
      while not isinstance(inp, bool):
        inp = input(display + "\nY/N (or nothing for default): ")
        if inp.upper() == "Y":
          inp = True
        elif inp.upper() == "N" or inp == "":
          inp = False
        else:
          print("input must be Y/N")
    elif type == self.DATE:
      for option in options:
        display += option
      while not isinstance(inp, dt.date):
        inp = input(display +  "\nEnter a date (YYYY-MM-DD) or nothing for default: ")
        if inp == "":
          return dt.date.today()
        inp = '-'.join(inp.split())
        try:
          print("trying to convert:", inp)
          inp = dt.datetime.strptime(inp, '%Y-%m-%d')
        except ValueError:
          print("error")
      inp = inp.date()
    elif type == self.INT:
      for option in options:
        display += option
      while not isinstance(inp, int):
        inp = input(display + "\nEnter a positive integer: ")
        try:
          inp = int(inp)
          if inp <= 0:
            print("Input must be a positive integer")
            inp = "error"
        except ValueError:
          print("enter an integer")
    else:
      print("unrecognized type")
    return inp

  def configure(self):
    email = ""
    while not email_validator.match(email):
      email = input("Enter a valid email to send notifications to: ")

    self.email = email

    use_default_settings = True
    inp = None
    while not isinstance(inp, bool):
      inp = input("Use default settings? (Y/N): ")
      if inp.upper() == "Y":
        inp = True
      elif inp.upper() == "N":
        inp = False
      else:
        print("input must be Y/N")
    
    use_default_settings = inp

    if not use_default_settings:
      self.property_type_id = self.getInput(["Any property type", "Apartment", "House", "Room"], self.STRING)
      self.lease_type_id = self.getInput(["Any lease type", "12 Month Lease", "8 Month Lease", "Sublet", "Assignment", "Other (e.g. monthly, short-term)"], self.STRING)
      self.number_of_rooms = self.getInput(["Any Number of Rooms", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight"], self.STRING)
      self.shared_accommodation = self.getInput(["Shared Accommodation"], self.BOOL)
      self.water_included = self.getInput(["Water Included"], self.BOOL)
      self.heat_included = self.getInput(["Heat Included"], self.BOOL)
      self.electricity_included = self.getInput(["Electricity Included"], self.BOOL)
      self.furnished = self.getInput(["Furnished"], self.BOOL)
      self.parking_available = self.getInput(["Parking Available"], self.BOOL)
      self.air_conditioning = self.getInput(["Air Conditioning"], self.BOOL)
      self.accessibility_features = self.getInput(["Accessibility Features"], self.BOOL)
      self.laundry_hookup = self.getInput(["Laundry Hookup"], self.BOOL)
      self.onsite_laundry = self.getInput(["Onsite Laundry"], self.BOOL)
      self.landlord_contract_program = self.getInput(["Landlord Contract Program"], self.BOOL)
      self.queens_owned = self.getInput(["University Owned"], self.BOOL)
      self.date_available = self.getInput(["Available After"], self.DATE)
      self.show_test = 0
      self.num_items = "all"
      self.frequency = self.getInput(["Polling Frequency (60 seconds or more recommended)"], self.INT)

  def current_settings(self):
    print('#' * 50)
    print(' ' * 18, 'SETTINGS')
    print('#' * 50)
    info = vars(self)
    for key in info:
      print(f'{key:<30} {info[key]}')
    print('#' * 50, '\n')

  def buildURL(self):
    url = self.BASE_API_URL
    settings = vars(self)
    for key in settings:
      if key == "listings" or key == "email":     # skip the non-url related fields
        continue
      
      if settings[key] is not None:
        url += f'{key}={settings[key]}&'          # concat the settings 
    
    if url[-1] == '&':
      url = url[:-1]

    return url

  def notify(self, listings):
    print(f'{len(listings)} new listings!')

    msg = EmailMessage()
    content = ''

    for listing in listings:
      content += listing.getContent()

    msg.set_content(f'<!DOCTYPE html><body><div style="display: block; justify-content: center; align-items: center; flex-direction: column;">{content}</div></body></html>', subtype='html')
    msg['Subject'] = f"New listing(s) on Queen's listings"
    msg['From'] = SENDER_ADDRESS
    msg['To'] = self.email

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    print('Email notification sent')

  def update_listings(self, string):
    string = string.replace('\\', '')
    sections = string.split('","')
    listing_section = sections[0][2:]
    parsed = BeautifulSoup(listing_section, 'html.parser')
    new_listings = []
    for row in parsed.find_all('tr'):      
      listing = Listing(row)
      if listing.address not in self.listings:
        # if its being monitored, send notification
        if self.active == True:
          new_listings.append(listing)
        
        self.listings[listing.address] = listing
      if self.test:
        new_listings.append(listing)
        self.test = len(new_listings) < 2
    if new_listings:
      self.notify(new_listings)
    print(f'Last checked at: {dt.datetime.now()}', end='\r')

  def query(self):
    response = requests.get(self.buildURL())
    self.update_listings(response.text)

  def start(self):
    Thread(target=self.monitor, args=()).start()
    return self

  def monitor(self):
    print(f'Starting to monitor at {dt.datetime.now()}, press q to exit')
    self.query()
    self.active = True
    has_tested = False
    while self.active:
      self.query()
      if not has_tested:
        self.test = True
        has_tested = True
      self.timer.wait(self.frequency)

  def stop(self):
    self.active = False
    self.timer.set()

  def display_listings(self):
    for address in self.listings:
      print('\n' + '#' * 100, '\n')
      self.listings[address].display()

def main():
  listing_manager = ListingManager()
  listing_manager.start()
  while True:
    if keyboard.read_key() == "q":
      listing_manager.stop()
      break

if __name__ == '__main__':
  main()
