import sys
sys.path.append('src')

from product import ProductUpdater

STORE_HASH = "5byitdbjtb"
API_TOKEN = "t4iu0pxpzxck0h5azrwmy8u3w9994q2"
BIGBUY_API_KEY = "NGQxYmVkZGU1ZTIxMGJjMzg4Yzk2MDNhYzUxNzhlNTNkYjAyMDQzYmU4YWFmYjA1ZWM1NzE0ODc2OWI4Y2I0MQ"

if __name__ == '__main__':
    updater = ProductUpdater(STORE_HASH, API_TOKEN, BIGBUY_API_KEY)
    product_file = "Products.json"
    prodcut_info_file = "ProductsInfo.json"
    image_file = "ImagesWithID.json"
    id_map_file = "ID_Mapping.json"
    variation_file = "Variations3.json"

    # data = updater.insert_products_to_bigcommerce(product_file, prodcut_info_file)
    # data = updater.create_images_in_bigcommerce(image_file)
    data = updater.create_variations_in_bigcommerce(variation_file)
    
    