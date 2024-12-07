"""Retrieving infromation from web scraping"""
import requests
import certifi
import pandas as pd
from bs4 import BeautifulSoup

# target URL
url = "https://bookings.lib.msu.edu/calendar/events/?cid=3079&t=g&d=0000-00-00&cal=3079&inc=0"
headers = {"User-Agent": "Mozilla/5.0"}

# use certifi path
try:
    response = requests.get(url, headers=headers, verify=certifi.where())
    print("successful data acquisition")
    print(response.text)
except requests.exceptions.SSLError as e:
    print(f"SSL authentication failed: {e}")
    # try to skip validation
    response = requests.get(url, headers=headers, verify=False)
    print("skip validation of the obtained data: ")
    print(response.text)



html_content = response.text

# use BeautifulSoup to analyze HTML
soup = BeautifulSoup(html_content, "html.parser")

# store event data
event_data = []

# find all active panels
event_panels = soup.find_all("div", class_="panel panel-default track")

for panel in event_panels:
    # extract activity name
    name_tag = panel.find("h3", class_="panel-title")
    event_name = name_tag.text.strip() if name_tag else "No Title"

    # extract activity date
    date_tag = panel.find("div", class_="date-header")
    event_date = date_tag.text.strip() if date_tag else "No Date"

    # extract activity description
    description_tag = panel.find("div", class_="description")
    description = description_tag.text.strip() if description_tag else "No Description"

    # extract registration link
    link_tag = panel.find("a", class_="pull-right btn btn-default")
    registration_link = link_tag['href'] if link_tag else "No Link"

    # store as dictionary
    event_data.append({
        "Event Name": event_name,
        "Date": event_date,
        "Description": description,
        "Registration Link": f"https://sessions.studentlife.umich.edu{registration_link}"
    })

# convert to a DataFrame
events_df = pd.DataFrame(event_data)

# also save as a CSV file
events_df.to_csv("events_data.csv", index=False, encoding="utf-8")
print("data saved to events_data.csv file")
