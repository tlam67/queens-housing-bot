import requests
import re
from bs4 import BeautifulSoup

class Listing:
  def __init__(self) -> None:
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
      img_url = row.img['src']
      print(img_url)
      data = row.find_all('td')
      for col in data[1:-1]:
        print(col.text)
      print(data[-1].a['href'])

response = requests.get('https://listingservice.housing.queensu.ca/public/getByFilter?property_type_id=&lease_type_id=&number_of_rooms=&shared_accommodation=false&water_included=false&heat_included=false&electricity_included=false&furnished=false&parking_available=false&air_conditioning=false&accessibility_features=false&laundry_hookup=false&onsite_laundry=false&landlord_contract_program=false&queens_owned=false&date_available=&show_test=0&num_items=10https://listingservice.housing.queensu.ca/public/getByFilter?property_type_id=&lease_type_id=&number_of_rooms=&shared_accommodation=false&water_included=false&heat_included=false&electricity_included=false&furnished=false&parking_available=false&air_conditioning=false&accessibility_features=false&laundry_hookup=false&onsite_laundry=false&landlord_contract_program=false&queens_owned=false&date_available=&show_test=0&num_items=1')

listing = Listing()

listing.parse(response.text)

# removeIrrelevant = re.compile('<(?!tr).*?>')
# separateEntries = re.compile('<tr.*?>')

# # print(cleanResponse(response.text))
# allButTD = re.compile('<(?!td).*?>')
# cleanHTML = re.compile('<.*?>')

# def cleanEntry(string: str):
#   removeHTML = re.sub(allButTD, '', string)
#   insertSeparators = re.sub(cleanHTML, '|', removeHTML)
#   return insertSeparators

# def test(resp: str):
#   split_content = resp.split('","')   # splits the sections of response
#   house_section = split_content[0][2:]        # get the section with all house info and remove first two chars ["
#   # removeHTML = re.sub(removeIrrelevant, '', house_section)
#   # clean = re.sub(separateEntries, '\n', removeHTML)

#   separated = house_section.split("<\/tr>")
#   separated.pop()   # remove empty last entry
#   cleaned = list(map(cleanEntry, separated))
#   return cleaned

# print(test(response.text))