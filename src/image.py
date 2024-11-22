import requests
import json

class ImageUpdater:
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

    # Get product image urls from file and save to BigCommerce. (ImagesWithID.json)
    def create_images_in_bigcommerce(self, image_file):
        with open(image_file, 'r') as f:
            product_image_data = json.load(f)
            for product_image in product_image_data[9554:100000]:
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

    # Get images from BigBuy for a product
    def get_image(self, product_id):
        url = f"{self.bigbuy_base_url}productimages/{product_id}"
            
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
    
    # Get new product id by sku
    def get_new_product_id(self, sku):
        url = f"{self.base_url}products?keyword={sku}"
            
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            if not 'data' in data:
                print("Error: No 'data' field")
                return 0

            if not isinstance(data['data'], list) or len(data['data']) < 1:
                print("Error: Invalid data")
                print(data)
                return 0
            
            return data['data'][0]['id']
            
        except requests.exceptions.HTTPError as err:
            print(f"Error: {err}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None

    # Get images from BigBuy for product and save to BigCommerce.
    def get_and_insert_image(self, product):
        product_id = product['id']
        product_sku = product['sku']

        # Get image from BigBuy
        image = self.get_image(product_id)

        if image is None:
            return
        
        if (not 'id' in image) or (not 'images' in image):
            return

        # Get new product id in BigCommerce
        new_product_id = self.get_new_product_id(product_sku)
        if new_product_id == 0:
            return

        images_data = image['images']
        for item in images_data:
            bigcommerce_data = {
                "image_url": item['url'],
                "is_thumbnail": True
            }

            # Create image in BigCommerce
            url = f"{self.base_url}products/{new_product_id}/images"
            response = requests.post(url, headers=self.headers, json=bigcommerce_data)
            if response.status_code == 200:
                print(f"image for {new_product_id} created successfully.")
            else:
                print(f"Error creating image {new_product_id}: {response.text}")
