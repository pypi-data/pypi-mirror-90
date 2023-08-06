import requests
import time

def getBTCHash():
    '''
    returns the most recent BTC hash
    '''
    url = 'https://blockchain.info/unconfirmed-transactions?format=json'
    object = requests.get(url, headers={'User-agent': 'bryson-bot'})
    object = object.json()
    hash = object['txs'][0]["hash"]
    return hash

def getETHHash():
    '''
    returns the most recent ETH hash
    '''
    session = requests.Session()
    url = "https://ropsten.infura.io/v3/7bc6c876fcb149a9ba7fdad033581e98"
    headers = {'Content-type': 'application/json'}

    blockNumber = "latest"
    # Boolean indicating if we want the full transactions (True) or just their hashes (false)
    fullTrx = False
    params = [ blockNumber, fullTrx]
    data = {"jsonrpc": "2.0", "method": "eth_getBlockByNumber","params": params, "id": 1}

    response = session.post(url, json=data, headers=headers)

    block = response.json().get("result")
    transactions = block.get("transactions")
    params = [transactions[0]]

    data = {"jsonrpc": "2.0", "method": "eth_getTransactionByHash","params": params, "id": 3}

    response = session.post(url, json=data, headers=headers)

    transaction = response.json().get("result")
    return transaction['hash']


def convertToNum(hash):
    '''
    Uses binary conversion to turn any string into a number
    '''
    hashBin = ' '.join(format(ord(x), 'b') for x in hash)
    hashBin = hashBin.replace(" ", "")
    binary = int(hashBin)

    decimal, i, n = 0, 0, 0
    while (binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1

    return decimal

def getRNG(btcHash,ethHash):
    '''
    randomizes number from two inputs and epoch time
    '''
    btcNum = convertToNum(btcHash)
    ethNum = convertToNum(ethHash)
    return (btcNum/ethNum) * time.time()

def random():
    return getRNG(getBTCHash(),getETHHash())

print(""""
 _______                                                    
|       \                                                   
| $$$$$$$\  ______   __    __   _______   ______   _______  
| $$__/ $$ /      \ |  \  |  \ /       \ /      \ |       \ 
| $$    $$|  $$$$$$\| $$  | $$|  $$$$$$$|  $$$$$$\| $$$$$$$\\
| $$$$$$$\| $$   \$$| $$  | $$ \$$    \ | $$  | $$| $$  | $$
| $$__/ $$| $$      | $$__/ $$ _\$$$$$$\| $$__/ $$| $$  | $$
| $$    $$| $$       \$$    $$|       $$ \$$    $$| $$  | $$
 \$$$$$$$  \$$       _\$$$$$$$ \$$$$$$$   \$$$$$$  \$$   \$$
                    |  \__| $$                              
                     \$$    $$                              
                      \$$$$$$                               
""")

print("Created by- Jonathan Zavialov")
print("Owned by the BRYSON collaborative. Visit us at http://bryson.studio/")
print("Thank you for installing BRYSON. Please run \"pip install -r requirements.txt\" for full installation.")