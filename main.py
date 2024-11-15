import sys
sys.path.append('src')

from product import ProductUpdater

STORE_HASH = "5byitdbjtb"
API_TOKEN = "t4iu0pxpzxck0h5azrwmy8u3w9994q2"
BIGBUY_API_KEY = "NGQxYmVkZGU1ZTIxMGJjMzg4Yzk2MDNhYzUxNzhlNTNkYjAyMDQzYmU4YWFmYjA1ZWM1NzE0ODc2OWI4Y2I0MQ"

if __name__ == '__main__':
    updater = ProductUpdater(STORE_HASH, API_TOKEN, BIGBUY_API_KEY)
    productFile = "Products.json"
    productInfoFile = "ProductsInfo.json"
    imageFile = "Image.json"
    idMapFile = "ID_Mapping.json"
    # data = updater.insert_products_to_bigcommerce(productFile, productInfoFile)
    # data = updater.create_variations_in_bigcommerce(productInfoFile)
    data = updater.create_images_in_bigcommerce(idMapFile, imageFile)
    
    