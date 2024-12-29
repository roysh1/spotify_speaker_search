from chatgpt_api import summarize_episode_content, get_guest_speaker, get_host
from spotify_api import get_spotify_episode

def format_results(episodes):
    results = []
    for episode in episodes:
        summary = summarize_episode_content(episode["description"])
        guests = get_guest_speaker(episode["description"])
        if length(guests) == 0:
            continue
        episode_content = get_spotify_episode()

        # host = get_host(episode["show"]["description"])
        results.append({
            "title": episode["name"],
            # "podcast": episode["show"]["name"],
            "summary": summary,
            # "host": host,
            "guests": guests,
            "url": episode["external_urls"]["spotify"]
        })
    return results
