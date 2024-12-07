"""Main driver"""
from config import EVENT_API_KEY, GPT_API_KEY
from events_api import get_events
from gpt_recommendation import generate_recommendations

def main():
    # User preferences (can be expanded or modified)
    preferences = {
        "race": "black",
        "age": "40",
        "favorite_song": "Wake Me Up When September Ends",
        "single_child_or_have_siblings": "single child",
    }

    # Fetch events from the Eventbrite API
    events = get_events(EVENT_API_KEY)
    if not events:
        print("No events found.")
        return

    # Get recommendations using GPT
    recommendations = generate_recommendations(events, preferences, GPT_API_KEY)
    if recommendations:
        print("\nRecommended events:")
        for event in recommendations:
            print(f"- {event}")
    else:
        print("No suitable recommendations found.")

if __name__ == "__main__":
    main()