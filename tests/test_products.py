import unittest
import sys
sys.path.append('src')
from product import ProductUpdater

STORE_HASH = "5byitdbjtb"
API_TOKEN = "fo5x9sykfda7kgw9m6jm6ljhwfljwkn"
BIGBUY_API_KEY = "NGQxYmVkZGU1ZTIxMGJjMzg4Yzk2MDNhYzUxNzhlNTNkYjAyMDQzYmU4YWFmYjA1ZWM1NzE0ODc2OWI4Y2I0MQ"

class TestProduct(unittest.TestCase):
    def test_add_positive_numbers(self):
        pu = ProductUpdater(STORE_HASH, API_TOKEN, BIGBUY_API_KEY)
        result = pu.add(2, 3)
        self.assertEqual(result, 5)

if __name__ == '__main__':
    unittest.main()
