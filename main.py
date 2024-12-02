import requests
import selectorlib
import sqlite3
from emailing import send_email

URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
YAML_PATH = "extract.yaml"
DATABASE_PATH = "data.db"
TABLE_NAME = "Events"

def scrape(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text

    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file(YAML_PATH)
    value = extractor.extract(source)["tours"]

    return value

def store_event(event):
    with sqlite3.connect(DATABASE_PATH) as connection:
        split = event.split(", ")
        performer, location, date = split
        cursor = connection.cursor()

        cursor.execute(f"INSERT INTO {TABLE_NAME} VALUES(?,?,?)", (performer, location, date))
        connection.commit()


def read_events():
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * from {TABLE_NAME}")
        events = cursor.fetchall()
        events = [", ".join(event) for event in events]

    return events

scraped = scrape(URL)
extracted = extract(scraped)

if extracted != "No upcoming tours":
    events = read_events()

    if extracted not in events:
        send_email(f"New event was found!\n{extracted}")
        store_event(extracted)