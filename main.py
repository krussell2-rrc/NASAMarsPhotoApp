"""
Program: NASA Mars Photo App
Author: Kareem Russell
Date: 2025-09-06
Description: This program connects to NASA’s Mars Rover Photos API, lets the user select a rover, prompts for a date,
and then retrieves and displays the photos taken by that rover on the specified day.
"""

from requests import get
import json
from dateutil.parser import parse
from PIL import Image
from io import BytesIO
from menu import Menu

API_KEY ='xKBYhH8wTdCpfdIup0tfpDraeGtOdNRwuKJ2W9J9'
photo_urls = []
image_options = []
last_selected = None

def display_photo(url):
  """
  Displays the photo found at the url

  Args:
    url: The url of the photo provided
  """
  img_resp = get(url)
  img = Image.open(BytesIO(img_resp.content))
  img.show()
  img.close()

  # Adds navigation options to the photosMenu after the user selects a photo
  global last_selected
  last_selected = photo_urls.index(url)

  navigation_options = [("Return to Main Menu", lambda: roverMenu.open())]

  if last_selected > 0:
      navigation_options.append(
          ("Back", lambda: display_photo(photo_urls[last_selected - 1]))
      )

  if last_selected < len(photo_urls) - 1:
      navigation_options.append(
          ("Next", lambda: display_photo(photo_urls[last_selected + 1]))
      )

  photosMenu.set_message("Browse through photos:")
  photosMenu.set_options(navigation_options)

def fetch_photos(rover):
  """
  Fetches the photo from the API based on the Rover selected and date provided

  Args:
    rover: The rover selected in the roverMenu
  """
  # Avoiding duplicates
  photo_urls.clear()

  date = parse(input(f"\nEnter the date you wanted to see pictures from taken by the {rover} Rover : ")).strftime("%Y-%m-%d")

  url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?earth_date={date}&api_key={API_KEY}"
  photos = get(url).json()

  # Getting the first 10 photos from the JSON
  for photo_url in photos['photos'][:10]:
      photo_urls.append(photo_url['img_src'])

  global image_options

  if(len(photo_urls) == 0):
    # Displaying message to try again or return to main menu if no rover photos are found
    photosMenu.set_message(f"There are no photos found on {date} for the {rover} Rover")
    image_options = [("Choose another date", lambda: fetch_photos(rover))] + [("Return to Main Menu", lambda: roverMenu.open())]
  else:
    # Displaying urls if rover photos are found
    photosMenu.set_message("Choose a photo to view:")
    image_options = [(url, lambda u=url: display_photo(u)) for url in photo_urls] + [("Return to Main Menu", lambda: roverMenu.open())]

  photosMenu.set_options(image_options)
  photosMenu.open()

photosMenu = Menu(
  title="Mars Rover Photo App",
  message="",
  prompt="> ",
  options=[]
)

roverMenu = Menu(
  title="Mars Rover Photo App",
  message="Choose a Rover:",
  prompt="> ",
  options=[
    ("Curiosity", lambda: fetch_photos("Curiosity")),
    ("Opportunity", lambda: fetch_photos("Opportunity")),
    ("Spirit", lambda: fetch_photos("Spirit")),
    ("Perseverance", lambda: fetch_photos("Perseverance"))
  ]
)

roverMenu.open()