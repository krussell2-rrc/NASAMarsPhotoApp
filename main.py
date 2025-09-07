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
  img_resp = get(url)
  img = Image.open(BytesIO(img_resp.content))
  img.show()
  img.close()

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
  photo_urls.clear()
  photosMenu.set_message("")

  date = parse(input(f"\nEnter the date you wanted to see pictures from taken by the {rover} Rover : ")).strftime("%Y-%m-%d")

  url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?earth_date={date}&api_key={API_KEY}"
  photos = get(url).json()

  for photo_url in photos['photos'][:10]:
      photo_urls.append(photo_url['img_src'])

  if(len(photo_urls) == 0):
    photosMenu.set_message(f"There are no photos found on {date} for the {rover} Rover")

  image_options = [
    (url, lambda u=url: display_photo(u)) for url in photo_urls
  ]

  photosMenu.set_options(image_options)
  photosMenu.open()

photosMenu = Menu(
  title="Mars Rover Photo App",
  message="Choose a photo to view:",
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