from bs4 import BeautifulSoup
import requests
import pandas as pd

credentials = ('USERNAME', 'PASSWORD')
url = "https://www.tripadvisor.fr/Search?q=Ile+Maurice&geo=1&ssrc=e&searchNearby=false&searchSessionId=000e783c7661d549.ssid&blockRedirect=true&offset=0"
payload = {
    'source': 'universal',
    'render': 'html',
    'url': url,
}
response = requests.post(
    'https://realtime.oxylabs.io/v1/queries',
    auth=credentials,
    json=payload,
)
print(response)
print(response.status_code)

content = response.json()["results"][0]["content"]
soup = BeautifulSoup(content, "html.parser")

data = []
for div in soup.find_all("div", {"class": "result"}):
    name = div.find('div', {"class": "result-title"}).find('span').get_text(strip=True)
    rating = div.find('span', {"class": "ui_bubble_rating"})['alt']

    review = div.find('a', {"class": "review_count"}).get_text(strip=True)
    data.append({
        "name": name,
        "rating": rating,
        "review": review,
    })
print(data)

df = pd.DataFrame(data)