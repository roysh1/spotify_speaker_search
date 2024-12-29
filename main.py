import csv
import os
from spotify_api import get_spotify_access_token, search_spotify_podcasts, get_spotify_episode
from chatgpt_api import extract_keywords_from_query, summarize_episode_content, get_host, get_guest_speaker
from utils import format_results

def main():
    # User query input
    query = input("Enter your search query: ")
    
    # Extract keywords
    # keywords = extract_keywords_from_query(query)
    # print(f"Extracted Keywords: {keywords}")
    
    # Authenticate with Spotify
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    access_token = get_spotify_access_token(client_id, client_secret)
    
    # Search podcasts
    items = []
    for i in range(1):
        items = items + search_spotify_podcasts(query, access_token, i*50)
    if not items:
        print("No relevant episodes found.")
        return

    episodes = []
    for item in items:
        episode = get_spotify_episode(item["id"], access_token)
        guests_dict = get_guest_speaker(episode["description"])
        if guests_dict["guests"] == "No guests":
            continue
        summary = summarize_episode_content(episode["description"], query)
        if summary == "irrelevant":
            continue
        host = get_host(episode["show"]["description"])
        episodes.append({
            "title": episode["name"],
            "podcast": episode["show"]["name"],
            "summary": summary,
            "host": host,
            "guests": guests_dict["guests"],
            "guest_info": guests_dict["info"],
            "url": episode["external_urls"]["spotify"],
            "date": episode["release_date"]
            })

    export_to_csv(episodes)



def export_to_csv(episodes):
    if episodes:
        with open("podcast_results2.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "podcast", "summary", "host", "guests", "guest_info", "date", "url"])
            writer.writeheader()
            writer.writerows(episodes)

        print("Results exported to podcast_results.csv")
    else:
        print("No episodes with guests were found.")

if __name__ == "__main__":
    main()
