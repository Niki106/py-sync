import requests
import json
import xml.etree.ElementTree as ET


class OrderSender:
    def __init__(self, store_hash, api_token, bigbuy_api_key):
        self.store_hash = store_hash
        self.api_token = api_token
        self.base_url = f"https://api.bigcommerce.com/stores/{self.store_hash}/v2/orders/"
        self.headers = {
            "X-Auth-Token": f"{self.api_token}"
        }
        self.bigbuy_base_url = f"https://api.bigbuy.eu/rest/catalog/"
        self.bigbuy_api_key = bigbuy_api_key
        self.bigbuy_headers = {
            "Authorization": f"Bearer {self.bigbuy_api_key}"
        }

    def get_xml_data(self, url):
        # url = f"{self.base_url}{order_id}"
            
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            xml_data = response.text
            root = ET.fromstring(xml_data)
            return root
            
        except requests.exceptions.HTTPError as err:
            print(f"Error: {err}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None
  
    def get_order_data(self, order_id):
        # Get order basic
        url = f"{self.base_url}{order_id}"
        basic = self.get_xml_data(url)
        
        # Get order products
        url = f"{self.base_url}{order_id}/products"
        products_root = self.get_xml_data(url)

        # Get order shipping addresses
        url = f"{self.base_url}{order_id}/shipping_addresses"
        shipping_addresses_root = self.get_xml_data(url)

        # Parse products
        products_json = []
        if products_root is None: return None

        for product in products_root:
            product_json = {}
            for child in product:
                if child.tag == 'quantity': product_json['quantity'] = child.text.strip() if child.text else ''
                if child.tag == 'sku': product_json['sku'] = child.text.strip() if child.text else ''
            
            products_json.append(product_json)
        
        # Parse shipping address
        shipping_address_json = {}
        if shipping_addresses_root is None: return None
        
        address = shipping_addresses_root.find('address')
        for child in address:
            if child.tag == 'first_name': shipping_address_json['firstName'] = child.text.strip() if child.text else ''
            if child.tag == 'last_name': shipping_address_json['lasttName'] = child.text.strip() if child.text else ''
            if child.tag == 'country_iso2': shipping_address_json['country'] = child.text.strip().lower() if child.text else ''
            if child.tag == 'email': shipping_address_json['email'] = child.text.strip() if child.text else ''
            if child.tag == 'city': shipping_address_json['town'] = child.text.strip() if child.text else ''
            if child.tag == 'street_1': shipping_address_json['address'] = child.text.strip() if child.text else ''
            if child.tag == 'zip': shipping_address_json['postcode'] = child.text.strip() if child.text else ''
            if child.tag == 'company': shipping_address_json['companyName'] = child.text.strip() if child.text else ''
            if child.tag == 'phone': shipping_address_json['phone'] = child.text.strip() if child.text else ''
            if child.tag == 'street1': shipping_address_json['address'] = child.text.strip() if child.text else ''

        # Prepare order data for BigBuy
        order_data = {}
        order_data['products'] = products_json
        order_data['shippingAddress'] = shipping_address_json
        order_data['internalReference'] = products_json
        order_data['language'] = 'en'
        order_data['paymentMethod'] = 'paypal'
        order_data['carriers'] = [{"name": "standard shipment"}]

        return order_data


    # Get variants from BigCommerce and send to BigBuy.
    def get_and_send_order(self, order_id):
        # Get order data from BigCommerce
        order_data = self.get_order_data(order_id)

        if order_data is None:
            return
        
        # Submit the order to BigBuy
        url = f"{self.bigbuy_base_url}products/{new_product_id}/variant"
        response = requests.post(url, headers=self.bigbuy_headers, json=order_data)
        if response.status_code == 200:
            print(f"Submitted the order successfully.")
        else:
            print(f"Error submitting order: {response.text}")

        