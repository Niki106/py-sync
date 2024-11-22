import sys
sys.path.append('src')

from product import ProductUpdater
from image import ImageUpdater
from variant import VariantUpdater
from taxonomy import TaxonomyUpdater

from synchronizer import Synchronizer

STORE_HASH = "5byitdbjtb"
API_TOKEN = "t4iu0pxpzxck0h5azrwmy8u3w9994q2"
BIGBUY_API_KEY = "NGQxYmVkZGU1ZTIxMGJjMzg4Yzk2MDNhYzUxNzhlNTNkYjAyMDQzYmU4YWFmYjA1ZWM1NzE0ODc2OWI4Y2I0MQ"

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <argument1>")
        sys.exit(1)

    synchronizer = Synchronizer(STORE_HASH, API_TOKEN, BIGBUY_API_KEY)

    action = sys.argv[1]
    if action == 'product':
        synchronizer.update_products()

    if action == 'category':
        synchronizer.update_categories()

if __name__ == '__main__':
    main()