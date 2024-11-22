import unittest
import sys
sys.path.append('src')
from taxonomy import TaxonomyUpdater

STORE_HASH = "5byitdbjtb"
API_TOKEN = "fo5x9sykfda7kgw9m6jm6ljhwfljwkn"
BIGBUY_API_KEY = "NGQxYmVkZGU1ZTIxMGJjMzg4Yzk2MDNhYzUxNzhlNTNkYjAyMDQzYmU4YWFmYjA1ZWM1NzE0ODc2OWI4Y2I0MQ"

class TestTaxonomy(unittest.TestCase):
    def test_add_positive_numbers(self):
        tu = TaxonomyUpdater(STORE_HASH, API_TOKEN, BIGBUY_API_KEY)
        result = tu.get_id_by_name('Computing')
        self.assertEqual(result, 19685)

if __name__ == '__main__':
    unittest.main()
