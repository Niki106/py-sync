import requests
import json

class ProductUpdater:
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

    # Read products from file and save to BigCommerce.
    def insert_products_to_bigcommerce(self, product_file, product_info_file):
        with open(product_file, 'r') as f:
            product_data = json.load(f)
            
            # Make dictionary with description and id
            product_price_dict = {}
            product_weight_dict = {}
            for product in product_data:
                product_price_dict[str(product['id'])] = product['retailPrice']
                product_weight_dict[str(product['id'])] = product['weight']

        with open(product_info_file, 'r') as f:
            product_info_data = json.load(f)
            
            count = 0
            for pinfo in product_info_data:
                count = count + 1
                if count < 4909:
                    continue

                product_name = pinfo['name']
                product_sku = pinfo['sku']
                product_categories = [2158]
                product_price = product_price_dict.get(str(pinfo['id']), 0)
                product_weight = product_weight_dict.get(str(pinfo['id']), 0)
                product_type = 'physical'
                product_availability = 'available'

                # Prepare BigCommerce product data
                bigcommerce_data = {
                    "name": product_name,
                    "sku": product_sku,
                    "categories": product_categories,
                    "price": product_price,
                    "weight": product_weight,
                    "type": product_type,
                    "availability": product_availability
                }

                # Create product in BigCommerce
                url = f"{self.base_url}products"
                response = requests.post(url, headers=self.headers, json=bigcommerce_data)
                if response.status_code == 200:
                    print(f"Product {product_name} created successfully.")
                else:
                    print(f"Error creating product {product_name}: {response.text}")


    def fetch_new_products_from_bigbuy(self):
        url = f"{self.bigbuy_base_url}new-products.json"
        
        try:
            bigbuy_response = requests.get(url, headers=self.bigbuy_headers)
            bigbuy_data = bigbuy_response.json()
            return bigbuy_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            return None  # Or handle the error differently, e.g., log the error, retry the request, etc.
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from BigBuy: {e}")
            return None

    
    def update_bigcommerce_object(self, object_type, object_id, data):
        url = f"{self.base_url}{object_type}/{object_id}"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for error HTTP statuses

    def update_object(self, object_type, object_id):
        bigbuy_data = self.fetch_data_from_bigbuy(object_id)
        # Map BigBuy data to BigCommerce fields
        bigcommerce_data = {
            "name": bigbuy_data["name"],
            "price": bigbuy_data["price"],
            # ... other fields as needed
        }
        self.update_bigcommerce_object(object_type, object_id, bigcommerce_data)
