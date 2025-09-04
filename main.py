from requests import get
import json
from dateutil.parser import parse
from PIL import Image
from io import BytesIO
from menu import Menu

API_KEY ='xKBYhH8wTdCpfdIup0tfpDraeGtOdNRwuKJ2W9J9'
photo_urls = []

def fetch_photos(rover):
  roverMenu.close()
  date = parse(input(f"\nEnter the date you wanted to see pictures from taken by the {rover} Rover : ")).strftime("%Y-%m-%d")

  url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?earth_date={date}&api_key={API_KEY}"
  photos = get(url).json()

  for photo_url in photos['photos']:
    photo_urls.append(photo_url['img_src'])


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