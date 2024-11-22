import requests
import json
import time

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
    def create_products_in_bigcommerce(self, product_file, product_info_file):
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
            
            for pinfo in product_info_data[294002:294253]:
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
                    print(f"Product {product_sku} created successfully.")
                else:
                    print(f"Error creating product {product_sku}: {response.text}")


        bigbuy_data = self.fetch_data_from_bigbuy(object_id)
        # Map BigBuy data to BigCommerce fields
        bigcommerce_data = {
            "name": bigbuy_data["name"],
            "price": bigbuy_data["price"],
            # ... other fields as needed
        }
        self.update_bigcommerce_object(object_type, object_id, bigcommerce_data)

    # Get new products from BigBuy for a parent taxonomy
    def get_new_products(self, parent_taxonomy):
        url = f"{self.bigbuy_base_url}new-products?parentTaxonomy={parent_taxonomy}?isoCode=en"
            
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

    # Get product info from BigBuy
    def get_product_name(self, sku):
        url = f"{self.bigbuy_base_url}productinformationbysku/{sku}?isoCode=en"
            
        try:
            response = requests.get(url, headers=self.bigbuy_headers)
            response.raise_for_status()
            data = response.json()

            if len(list(data)) < 1: 
                print("Empty result")
                return ''
            
            return data[0]['name']
        except requests.exceptions.HTTPError as err:
            print(f"Error: {err}")
            return ''
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return ''
    
    # Insert the product to BigCommerce.
    def insert_product(self, product):
        product_sku = product['sku']
        product_name = self.get_product_name(product_sku)
        if product_name == '': return

        bigcommerce_data = {
            "name": self.get_product_name(product_sku),
            "sku": product_sku,
            "categories": [2158],
            "price": product['retailPrice'],
            "weight": product['weight'],
            "type": 'physical',
            "availability": 'available'
        }

        # Create product in BigCommerce
        url = f"{self.base_url}products"
        response = requests.post(url, headers=self.headers, json=bigcommerce_data)
        if response.status_code == 200:
            print(f"Product {product_sku} created successfully.")
        else:
            print(f"Error creating product {product_sku}: {response.text}")

