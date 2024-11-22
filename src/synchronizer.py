import sys
sys.path.append('src')

from taxonomy import TaxonomyUpdater
from product import ProductUpdater
from image import ImageUpdater
from variant import VariantUpdater

class Synchronizer:
    def __init__(self, store_hash, api_token, bigbuy_api_key):
        self.taxonomy_updater = TaxonomyUpdater(store_hash, api_token, bigbuy_api_key)
        self.product_updater = ProductUpdater(store_hash, api_token, bigbuy_api_key)
        self.image_updater = ImageUpdater(store_hash, api_token, bigbuy_api_key)
        self.variant_updater = VariantUpdater(store_hash, api_token, bigbuy_api_key)

    # Get new products from BigBuy and save to BigCommerce.
    def create_new_products(self, taxonomy):
        products = self.product_updater.get_new_products(taxonomy)
        if products is not None:
            for product in products:
                sku = product['sku']
                # Create product
                self.product_updater.insert_product(product)

                # Insert images for the product
                self.image_updater.get_and_insert_image(product)

                # Insert variants for the product
                self.variant_updater.get_and_insert_variant(product)

                break
        
        print(f"Products for taxonomy {taxonomy} have been updated.")
            
    # Update products in BigCommerce with data from BigBuy
    def update_products(self):
        # 19531: 'Electronics', 19685: 'Computing', 19651: 'DIY and tools', 19678: 'GPS devices'
        # Can get these IDs by using get_id_by_name method of TaxonomyUpdater class
        taxonomies = [16313, 19685, 19651, 19678] 
        for taxonomy in taxonomies:
            self.create_new_products(taxonomy)

    def update_categories(self):
        print("I am updating categories")