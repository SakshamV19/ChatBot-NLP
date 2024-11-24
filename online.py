import requests
import json

# Function to search Google and extract snippets from the first 25 search results
def search_google(query):
    # Set up the API request parameters
    api_key = 'AIzaSyCNG2cPvDJozyGGMBdSUFp2i2cHMl8FSVg'
    cse_id = '5090338d5a32748af'
    url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cse_id}&q={query}'

    # Send the API request and parse the JSON response
    response = requests.get(url)
    data = json.loads(response.text)

    # Extract snippets from the first 25 search results
    snippets = []
    for item in data.get('items', [])[:25]:
        snippet = item.get('snippet', '')
        snippets.append(snippet)

    return snippets