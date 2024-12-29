import csv
import os
import spotify_api
import chatgpt_api


def export_to_csv(episodes):
    if episodes:
        with open("podcast_results2.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "podcast", "summary", "host", "guests", "guest_info", "date", "url"])
            writer.writeheader()
            writer.writerows(episodes)

        print("Results exported to podcast_results.csv")
    else:
        print("No episodes with guests were found.")


def main():
    # User query input
    query = input("Enter your search query: ")
        
    # Authenticate with Spotify
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    access_token = spotify_api.get_spotify_access_token(client_id, client_secret)
    
    items = spotify_api.search_spotify_podcasts(10, access_token)

    episodes = []
    for item in items:
        episode = spotify_api.get_spotify_episode(item["id"], access_token)
        guests_dict = chatgpt_api.get_guest_speaker(episode["description"])
        if guests_dict["guests"] == "No guest":
            continue
        summary = chatgpt_api.summarize_episode_content(episode["description"], query)
        if summary == "irrelevant":
            continue
        host = chatgpt_api.get_host(episode["show"]["description"])
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



if __name__ == "__main__":
    main()