"""Get GPT's recommendations based on events and preferences"""
import openai
from events_api import format_event

def generate_recommendations(events, preferences, gpt_api_key):
    openai.api_key = gpt_api_key

    # Format preferences into a string
    preferences_text = (
        f"Race: {preferences['race']}, Age: {preferences['age']}, "
        f"Favorite Song: {preferences['favorite_song']}, "
        f"Single Child or Have Siblings: {preferences['single_child_or_have_siblings']}"
    )
    # Format the events into a readable list
    formatted_events = format_event(events)

    # Prompt for GPT
    prompt = f"""
    Here is a list of campus events:
    {formatted_events}

    Based on the user's preferences: {preferences_text}, recommend the top 3 events and explain why each event is a good match.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Or "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7,  # Adjust creativity level
        )
        recommendations = response["choices"][0]["message"]["content"]
        return recommendations.split("\n")  # Split into individual recommendations
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return []
