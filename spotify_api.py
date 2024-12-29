import requests
import base64
from concurrent.futures import ThreadPoolExecutor

def get_spotify_access_token(client_id, client_secret):
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(auth_url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def get_podcasts(keywords, access_token, offset=0):
    search_url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "q": keywords,
        "type": "episode",
        "limit": 50,
        "offset": offset
    }
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get("episodes", {}).get("items", [])

def search_spotify_podcasts(query, num_iterations, access_token):
    offsets = [i * 50 for i in range(num_iterations)]
    results = []

    def fetch(offset):
        return get_podcasts(query, access_token, offset)

    with ThreadPoolExecutor(max_workers=num_iterations) as executor:
        futures = [executor.submit(fetch, offset) for offset in offsets]
        for future in futures:
            try:
                results.extend(future.result())
            except Exception as e:
                print(f"Error fetching podcasts for offset {offset}: {e}")
    
    if not results:
        print("No relevant episodes found.")
        return []

    episodes = []

    def fetch_episode_details(episode):
        return get_spotify_episode(episode["id"], access_token)

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(fetch_episode_details, result) for result in results]
        for future in futures:
            try:
                episodes.append(future.result())
            except Exception as e:
                print(f"Error fetching episode details: {e}")


    return episodes

def get_spotify_episode(episode_id, access_token):
    episode_url = f"https://api.spotify.com/v1/episodes/{episode_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(episode_url, headers=headers)
    response.raise_for_status()
    return response.json()