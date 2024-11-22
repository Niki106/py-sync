from src import order

STORE_HASH = "5byitdbjtb"
API_TOKEN = "t4iu0pxpzxck0h5azrwmy8u3w9994q2"
BIGBUY_API_KEY = "YzhmYWFlMDFjMTA2YTZjZjRhYzhjMjg1NGViOGUwYTYzYjk1YTNjOGY4MDY3NzM1NzgyNzNhNzhiMDY5NGJiZA"  # sandbox

order_sender = order.OrderSender(STORE_HASH, API_TOKEN, BIGBUY_API_KEY)
order_data = order_sender.get_order_data(104)
print(order_data)

