This repo uses the spotify API and the OpenAI API in order to look for people that were guests on podcasts in a subject of interest.
In order to use it, get a secret key for both Spotify API and OpenAI API and save them as env variables:
- SPOTIFY_CLIENT_ID
- SPOTIFY_CLIENT_SECRET
- OPENAI_API_KEY
Then write your search query, and it will export the results into a CSV file with the relevant podcasts and their guests.
