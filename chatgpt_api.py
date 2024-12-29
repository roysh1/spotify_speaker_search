from openai import OpenAI
import json

client = OpenAI()

def completion(query):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {"role": "user", "content": query}
        ],
        response_format={
            "type": "text"
        },

    )
    return response.choices[0].message.content

def extract_keywords_from_query(query):
    return completion(f"Extract important keywords or topics from this query for searching podcasts: {query}")

def summarize_episode_content(description, query):
    return completion(f"Summarize this podcast episode description in 2 sentences: {description}, if it isn't really relevant for my search, which was {query}, return 'irrelevant'")

def get_guest_speaker(description):
    guests = completion(f"Get the guest speaker (or guest speakers) from the following podcast episode description. If there is more information about the guest (what they do), write the info about the guest as well. The response format should be a json object (without tags saying it's json or anything) where the first key is 'guests' and the value is the first and last name (or names) the next key should be 'info' and the value should be other info about the guests. If no explicit guest is mentioned, the value of guests should be 'No guest': {description}")
    try:
        guests_dict = json.loads(guests)
    except Exception as e:
        return {"guests": "No guest", "info": ""}
    return guests_dict

def get_host(description):
    return completion(f"Get the host of the podcast from the following podcast show description. If no explicit host is mentioned, return 'No host': {description}")
    