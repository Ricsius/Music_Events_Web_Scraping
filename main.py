import requests
import selectorlib
import os.path

URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
YAML_PATH = "extract.yaml"
EVENTS_PATH = "data.txt"

def scrape(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text

    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file(YAML_PATH)
    value = extractor.extract(source)["tours"]

    return value

def send_email():
    print("Email was sent")

def store_event(event):
    with open(EVENTS_PATH, "a") as file:
        file.write(event + "\n")

def read_events():
    if not os.path.isfile(EVENTS_PATH):
        return []
    
    with open(EVENTS_PATH, "r") as file:
        events = [event.strip() for event in file.readlines()]

    return events

scraped = scrape(URL)
extracted = extract(scraped)

if extracted != "No upcoming tours":
    events = read_events()

    if extracted not in events:
        send_email()
        store_event(extracted)