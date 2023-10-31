
import requests
import time

MONGO_URL="mongodb://localhost:27017/"
MONGO_DB="Dubizzle_Qatar"
URL="dubizzle_urls"
DATA="dubizzle_datas"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

def retry_request(url, max_retries=5, retry_delay=3):
    for _ in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            if response.status_code == 200:
                return response
        except requests.exceptions.RequestException as e:
            print(f"Failed to make a request: {str(e)}")
        print(f"Retrying request to {url}...")
        time.sleep(retry_delay)
    return None




