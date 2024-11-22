import requests
import json

class TaxonomyUpdater:
    def __init__(self, store_hash, api_token, bigbuy_api_key):
        self.store_hash = store_hash
        self.api_token = api_token
        self.base_url = f"https://api.bigcommerce.com/stores/{self.store_hash}/v3/catalog/"
        self.headers = {
            "X-Auth-Token": f"{self.api_token}"
        }
        self.bigbuy_base_url = f"https://api.bigbuy.eu/rest/catalog/"
        self.bigbuy_api_key = bigbuy_api_key
        self.bigbuy_headers = {
            "Authorization": f"Bearer {self.bigbuy_api_key}"
        }

    # Get taxonomy ID from BigBuy by names
    def get_all(self):
        url = f"{self.bigbuy_base_url}taxonomies?isoCode=en"
            
        try:
            response = requests.get(url, headers=self.bigbuy_headers)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.HTTPError as err:
            print(f"Error: {err}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None

    # Get taxonomy ID from BigBuy by names
    def get_id_by_name(self, name):
        taxonomies = self.get_all()

        if taxonomies is None:
            return 0    # No taxonomies
        
        for taxonomy in taxonomies:
            if taxonomy['name'] == name:
                return taxonomy['id']
        
        return 0