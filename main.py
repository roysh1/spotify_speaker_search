import csv
import os
import spotify_api
import chatgpt_api
from concurrent.futures import ThreadPoolExecutor


def export_to_csv(episodes):
    if episodes:
        with open("podcast_results2.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "podcast", "summary", "host", "guests", "guest_info", "date", "url"])
            writer.writeheader()
            writer.writerows(episodes)

        print("Results exported to podcast_results.csv")
    else:
        print("No episodes with guests were found.")


def process_episode(item, query):
    """
    Process a single episode: get guest speakers, summarize content, and extract the host.
    Returns a dictionary with the processed results or None if irrelevant.
    """
    guests_dict = chatgpt_api.get_guest_speaker(item["description"])
    if guests_dict["guests"] == "No guest":
        return None

    summary = chatgpt_api.summarize_episode_content(item["description"], query)
    if summary == "irrelevant":
        return None

    host = chatgpt_api.get_host(item["show"]["description"])
    return {
        "title": item["name"],
        "podcast": item["show"]["name"],
        "summary": summary,
        "host": host,
        "guests": guests_dict["guests"],
        "guest_info": guests_dict["info"],
        "url": item["external_urls"]["spotify"],
        "date": item["release_date"]
    }

def process_episodes_multi_threaded(items, query):
    """
    Multi-threaded processing of episodes.
    Returns a list of processed episodes.
    """
    processed_results = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(process_episode, item, query) for item in items]
        for future in futures:
            try:
                result = future.result()
                if result:
                    processed_results.append(result)
            except Exception as e:
                print(f"Error processing episode: {e}")

    return processed_results



def main():
    # User query input
    query = input("Enter your search query: ")
        
    # Authenticate with Spotify
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    access_token = spotify_api.get_spotify_access_token(client_id, client_secret)
    
    items = spotify_api.search_spotify_podcasts(query, 2, access_token)
    processed_episodes = process_episodes_multi_threaded(items, query)

    export_to_csv(processed_episodes)



if __name__ == "__main__":
    main()