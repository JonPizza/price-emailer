import smtplib
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from time import sleep

email_addrs = [] # PUT A LIST OF EMAILS TO SEND TO HERE

your_api_key = '' # Your CoinMarketCap API key, the free version is plenty
sender_addr = '' # Your Email Address
sender_pwd = '' # Your Email's Password

days = 2 # Days in between send

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(sender_addr, sender_pwd)


def send_email(btc_p, eth_p, ltc_p, rvn_p):
	for eml in email_addrs:
		name = eml.split('@')[0]
    # EDIT THE MESSAGE HERE <---------------------------------------------------------------------< EDIT MESSAGE
		msg = f"""Subject: Crypto Price Update

Howdy {name}!

The Prices are as follows:
Bitcoin: ${btc_p}
Ethereum: ${eth_p}
Litecoin: ${ltc_p}
Ravencoin: ${rvn_p}
"""

		#server.sendmail(sender_addr, eml, msg)

		print(f'Email sent to {eml}')

	server.quit()


url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
	'start': '1',
	'limit': 2000,



	'convert': 'USD',
	'sort': 'name'
}
headers = {
	'Accepts': 'application/json',
	'X-CMC_PRO_API_KEY': your_api_key,
}


def indexer(data):
	dat = data
	x=0

	total_data = []

	for i in dat:
		if i['symbol'] == 'BTC' or i['symbol'] == 'ETH' or i['symbol'] == 'LTC' or i['symbol'] == 'RVN':
			total_data.append(x)
		x+=1

	return total_data

while True:
	try:
		session = Session()
		session.headers.update(headers)
		
		response = session.get(url, params=parameters)
		data = json.loads(response.text)['data']
		
		send_email(round(data[indexer(data)[0]]['quote']['USD']['price'], 3), round(data[indexer(data)[0]]['quote']['USD']['price'],3), round(data[indexer(data)[0]]['quote']['USD']['price'], 3), round(data[indexer(data)[0]]['quote']['USD']['price'], 3))

	except (ConnectionError, Timeout, TooManyRedirects) as e:
		print(e)

	sleep(86400*days)
