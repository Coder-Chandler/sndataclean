from binance.client import Client

api_key = "2f002f83-c3744179-72cf4820-ec29f"
api_secret = "047b09bb-c524a3fd-34011eae-8aeea"

client = Client(api_key, api_secret)

coin = "XRP"

# 获取X-ETH数量、价格
x_eth_depth = client.get_order_book(symbol= coin+'ETH')
# asks 要卖的人 我们对他的买  需要低价       【买入】
x_eth_price = x_eth_depth["asks"][0][0]
x_eth_num = x_eth_depth["asks"][0][1]

print("X-ETH价格：{}".format(x_eth_price))
print("X-ETH数量：{}".format(x_eth_num))