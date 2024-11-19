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

    # Get product image urls from file and save to BigCommerce.
    def create_images_in_bigcommerce(self, image_file):
        with open(image_file, 'r') as f:
            product_image_data = json.load(f)
            for product_image in product_image_data[10000:200000]:
                new_product_id = product_image['new_id']
                
                # Create product image in BigCommerce
                images = product_image['images']
                for image in images:
                    img_url = image['url']
                    is_thumbnail = True
                    
                    bigcommerce_data = {
                        "image_url": img_url,
                        "is_thumbnail": is_thumbnail
                    }

                    try:
                        url = f"{self.base_url}products/{new_product_id}/images"
                        response = requests.post(url, headers=self.headers, json=bigcommerce_data)
                        if response.status_code == 200:
                            print(f"Image for {new_product_id} created successfully.")
                    except (json.JSONDecodeError, requests.exceptions.RequestException) as e:
                        print(f"Error creating image {new_product_id}: {response.text}")
    
    # Get product variations from BigBuy and create in BigCommerce
    def create_variations_in_bigcommerce(self, variation_file):
        with open(variation_file, 'r') as f:
            variation_data = json.load(f)
            variation_dict = dict(variation_data)
            variation_list = list(variation_dict)
            for product_id in variation_list[0:1]:
                variations = variation_dict[product_id]
                
                for index, variation in enumerate(variations):
                    # Create project option
                    bigcommerce_data = {
                        "display_name": f"Option_{index}",
                        "type": "radio_buttons",
                        "option_values": [
                            {
                                "is_default": False,
                                "label": f"Green {index}",
                                "sort_order": 0,
                                "value_data": {},
                                "id": 0
                            }
                        ]
                    }

                    url = f"{self.base_url}products/{product_id}/options"
                    response = requests.post(url, headers=self.headers, json=bigcommerce_data)

                    if response.status_code != 200: 
                        print(response.status_code, response.text)
                        continue    # Can't add option

                    option = response.json()

                    option_id = option['data']['id']
                    value_id = option['data']['option_values'][0]['id']
                     
                    # Create variations in BigCommerce
                    price = variation['inShopsPrice']
                    sale_price = variation['wholesalePrice']
                    retail_price = variation['retailPrice']
                    sku = variation['sku']
                    width = variation['width']
                    height = variation['height']
                    depth = variation['depth']

                    # Prepare BigCommerce variation data
                    bigcommerce_data = {
                        "price": price,
                        "sale_price": sale_price,
                        "retail_price": retail_price,
                        "sku": sku,
                        "weight": width,
                        "height": height,
                        "depth": depth,
                        "product_id": product_id,
                        "option_values": [
                            {
                                "option_id": option_id,
                                "id": value_id
                            }
                        ]
                    }

                    print(index, bigcommerce_data)
                   
                    # Create variation in BigCommerce
                    url = f"{self.base_url}products/{product_id}/variants"
                    response = requests.post(url, headers=self.headers, json=bigcommerce_data)
                    if response.status_code == 200:
                        print(f"Variant for {product_id} created successfully.")
                    else:
                        print(f"Error creating variation {product_id}: {response.text}")
                                        
                # Do one product only
                break
    
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
