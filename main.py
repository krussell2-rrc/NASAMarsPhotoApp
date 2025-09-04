from requests import get
import json
from dateutil.parser import parse
from PIL import Image
from io import BytesIO
from menu import Menu

def selected_rover(rover):
  roverMenu.close()
  date = parse(input(f"\nEnter the date you wanted to see pictures from taken by the {rover} Rover : ")).strftime("%Y-%m-%d")

roverMenu = Menu(
  title="Mars Rover Photo App",
  message="Choose a Rover:",
  prompt="> ",
  options=[
    ("Curiosity", lambda: selected_rover("Curiosity")),
    ("Opportunity", lambda: selected_rover("Opportunity")),
    ("Spirit", lambda: selected_rover("Spirit")),
    ("Perseverance", lambda: selected_rover("Perseverance"))
  ]
)

roverMenu.open()