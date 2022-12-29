import requests
from bs4 import BeautifulSoup

class Listing:
  def __init__(self) -> None:
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

  def parse(self, string):
    string = string.replace('\\', '')
    sections = string.split('","')
    listing_section = sections[0][2:]
    parsed = BeautifulSoup(listing_section, 'html.parser')
    for row in parsed.find_all('tr'):      
      data = row.find_all('td')
      if len(data) != 10:
        print("not length 10, unknown format")
        return
      
      self.img = row.img['src']
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

response = requests.get('https://listingservice.housing.queensu.ca/public/getByFilter?property_type_id=&lease_type_id=&number_of_rooms=&shared_accommodation=false&water_included=false&heat_included=false&electricity_included=false&furnished=false&parking_available=false&air_conditioning=false&accessibility_features=false&laundry_hookup=false&onsite_laundry=false&landlord_contract_program=false&queens_owned=false&date_available=&show_test=0&num_items=10https://listingservice.housing.queensu.ca/public/getByFilter?property_type_id=&lease_type_id=&number_of_rooms=&shared_accommodation=false&water_included=false&heat_included=false&electricity_included=false&furnished=false&parking_available=false&air_conditioning=false&accessibility_features=false&laundry_hookup=false&onsite_laundry=false&landlord_contract_program=false&queens_owned=false&date_available=&show_test=0&num_items=1')

listing = Listing()

listing.parse(response.text)
listing.display()
