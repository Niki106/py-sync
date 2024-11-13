import sys
sys.path.append('src')

from product import ProductUpdater
from category import CategoryUpdater

STORE_HASH = "5byitdbjtb"
API_TOKEN = "t4iu0pxpzxck0h5azrwmy8u3w9994q2"
BIGBUY_API_KEY = "NGQxYmVkZGU1ZTIxMGJjMzg4Yzk2MDNhYzUxNzhlNTNkYjAyMDQzYmU4YWFmYjA1ZWM1NzE0ODc2OWI4Y2I0MQ"

if __name__ == '__main__':
    updater = ProductUpdater(STORE_HASH, API_TOKEN, BIGBUY_API_KEY)
    productFile = "D:\\Work\\Python\\Abdulrahman\\Data\\BigBuy\\Products.json"
    productInfoFile = "D:\\Work\\Python\\Abdulrahman\\Data\\BigBuy\\ProductsInfo.json"
    data = updater.insert_products_to_bigcommerce(productFile, productInfoFile)
    
    