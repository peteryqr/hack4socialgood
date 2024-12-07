"""Retrieving infromation from eventbrite's API"""
import requests
import time
from config import EVENT_API_URL
'''
this is for retrieving events infromation from eventbrite API
'''

def get_events(api_key, retries=3, delay=2):
    """
    Fetch all available events from the Eventbrite API.

    Parameters:
        api_key (str): Your Eventbrite API key.
        retries (int): Number of retry attempts if the API request fails.
        delay (int): Delay (in seconds) between retries.

    Returns:
        list: A list of events if the request is successful, or None if it fails.
    """
    # Define HTTP headers
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    # Define API request parameters
    params = {
        'status': 'live',  # Fetch only live events
    }

    # Retry logic
    for attempt in range(retries):
        try:
            response = requests.get(EVENT_API_URL, headers=headers, params=params)
            if response.status_code == 200:
                # Return the list of events
                return response.json().get('events', [])
            else:
                print(f"Attempt {attempt + 1} failed: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Error during request: {e}")
        
        # Exponential backoff
        time.sleep(delay * (attempt + 1))

    # Return None if all retries fail
    return None

def format_event(event):
    """
    Format a single event into a readable string.

    Parameters:
        event (dict): Event data from the API response.

    Returns:
        str: Formatted event details.
    """
    name = event['name']['text'] if event['name'] else 'No name available'
    description = event['description']['text'] if event.get('description') else 'No description available'
    start_time = event['start']['local'] if event.get('start') else 'Unknown start time'
    end_time = event['end']['local'] if event.get('end') else 'Unknown end time'
    url = event.get('url', 'No URL available')
    # Fetch venue/location information if available
    venue = event.get('venue', {})
    location = f"{venue.get('address', {}).get('localized_address_display', 'Location not available')}"

    return (
        f"Event Name: {name}\n"
        f"Description: {description}\n"
        f"Start Time: {start_time}\n"
        f"End Time: {end_time}\n"
        f"Location: {location}\n"
        f"URL: {url}\n"
    )