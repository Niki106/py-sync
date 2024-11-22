import requests
import json

class VariantUpdater:
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

    def create_product_option(self, product_id):
        # Create project option
        bigcommerce_data = {
            "display_name": f"Default Option",
            "type": "radio_buttons",
            "option_values": [
                {
                    "is_default": False,
                    "label": f"WAge",
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
            return None
        
        return response.json()

    # Read product variations from file and create in BigCommerce (Variations3.json)
    def create_variations_in_bigcommerce(self, variation_file):
        with open(variation_file, 'r') as f:
            variation_data = json.load(f)
            variation_dict = dict(variation_data)
            variation_list = list(variation_dict)
            for product_id in variation_list:
                variations = variation_dict[product_id]

                option = self.create_product_option(int(product_id))
                if option is None: continue                

                option_id = option['data']['id']
                value_id = option['data']['option_values'][0]['id']
                                            
                for index, variation in enumerate(variations):
                    # # Create an option value for this variant
                    # bigcommerce_data = {
                    #     "label": f"Age {index}",
                    #     "sort_order": 0,
                    #     "value_data": {
                    #         "age": index
                    #     },
                    #     "is_default": False
                    # }

                    # url = f"{self.base_url}products/{product_id}/options/{option_id}/values"
                    # response = requests.post(url, headers=self.headers, json=bigcommerce_data)
                    # value = response.json()
                    # value_id = value['data']['id']
                                        
                    # Prepare BigCommerce variation data
                    bigcommerce_data = {
                        "price": variation['inShopsPrice'],
                        "sale_price": variation['salesPrice'],
                        "retail_price": variation['retailPrice'],
                        "sku": variation['sku'],
                        "weight": variation['weight'],
                        "height": variation['height'],
                        "depth": variation['depth'],
                                "product_id": product_id,
                        "option_values": [
                            {
                                "option_id": option_id,
                                "id": value_id
                            }
                        ]
                    }

                    # Create variation in BigCommerce
                    url = f"{self.base_url}products/{product_id}/variants"
                    response = requests.post(url, headers=self.headers, json=bigcommerce_data)
                    if response.status_code == 200:
                        print(f"Variant for {product_id} created successfully.")
                    else:
                        print(f"Error creating variation {product_id}: {response.text}")
                                        
                    # Do one variation only
                    break

    # Get variations from BigBuy for a product
    def get_variation(self, product_id):
        url = f"{self.bigbuy_base_url}productvariations/{product_id}"
            
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

    # Get variants from BigBuy for product and save to BigCommerce.
    def get_and_insert_variant(self, product):
        product_id = product['id']
        product_sku = product['sku']

        # Get variation from BigBuy
        variation = self.get_variation(product_id)

        if variation is None:
            return
        
        if (not 'data' in variation):
            return

        # Get new product id in BigCommerce
        new_product_id = self.get_new_product_id(product_sku)
        if new_product_id == 0:
            return

        option = self.create_product_option(product_id)
        if option is None: return                

        option_id = option['data']['id']
        value_id = option['data']['option_values'][0]['id']

        variants_data = variation['data']
        for item in variants_data:
            bigcommerce_data = {
                "price": variation['inShopsPrice'],
                "sale_price": variation['salesPrice'],
                "retail_price": variation['retailPrice'],
                "sku": variation['sku'],
                "weight": variation['weight'],
                "height": variation['height'],
                "depth": variation['depth'],
                "product_id": product_id,
                "option_values": [
                    {
                        "option_id": option_id,
                        "id": value_id
                    }
                ]
            }

            # Create variant in BigCommerce
            url = f"{self.base_url}products/{new_product_id}/variant"
            response = requests.post(url, headers=self.headers, json=bigcommerce_data)
            if response.status_code == 200:
                print(f"Variant for {new_product_id} created successfully.")
            else:
                print(f"Error creating varinat {new_product_id}: {response.text}")

            # Do one variant only
            break
