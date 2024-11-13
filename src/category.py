import requests
import json

class CategoryUpdater:
    def __init__(self, store_hash, api_token, bigbuy_api_key):
        self.store_hash = store_hash
        self.api_token = api_token
        self.base_url = f"https://api.bigcommerce.com/stores/{self.store_hash}/v3/"
        self.headers = {
            "X-Auth-Token": f"{self.api_token}"
        }
        self.bigbuy_base_url = f"https://api.bigbuy.eu/rest/catalog/"
        self.bigbuy_api_key = bigbuy_api_key
        self.bigbuy_headers = {
            "Authorization": f"Bearer {self.bigbuy_api_key}"
        }

    # Read categories from file and save to BigCommerce.
    def insert_categories_to_bigcommerce(self, json_file_path):
        with open(json_file_path, 'r') as f:
            categories_data = json.load(f)

            for cateogry in categories_data:
                cateogry_id = cateogry['id']
                cateogry_name = cateogry['name']
                cateogry_parent_id = cateogry['parentCategory']
                
                # Prepare BigCommerce category data
                bigcommerce_data = {
                    "name": cateogry_name,
                    "description": str(cateogry_id),
                    "meta_description": str(cateogry_parent_id),
                    "parent_id": 0 #cateogry_parent_id,
                    # "image_url": cateogry_image_url
                }

                # Create category in BigCommerce
                url = f"{self.base_url}catalog/categories"
                response = requests.post(url, headers=self.headers, json=bigcommerce_data)

                if response.status_code == 200:
                    print(f"Product {cateogry_name} created successfully.")
                else:
                    print(f"Error creating product {cateogry_name}")

    # Read categories from file and update BigCommerce. (parent_id, image)
    def update_categories_to_bigcommerce(self, json_file_path):
        with open(json_file_path, 'r') as f:
            categories_data = json.load(f)
            
            # Make dictionary with description and id
            category_dict = {}
            for category in categories_data:
                category_dict[category['description']] = category['category_id']
    
            for cateogry in categories_data:
                category_id = cateogry['category_id']
                # if (category_id < 2733):
                #     continue
                
                old_parent_id = cateogry['meta_description']
                new_parent_id = category_dict.get(old_parent_id, 0)
                
                
                bigcommerce_data = {
                    "parent_id": new_parent_id
                }

                url = f"{self.base_url}catalog/categories/{category_id}"
                response = requests.put(url, headers=self.headers, json=bigcommerce_data)

                if response.status_code == 200:
                    print(f"Category {category_id} updated successfully.")
                else:
                    print(f"Error updating product {category_id}")
