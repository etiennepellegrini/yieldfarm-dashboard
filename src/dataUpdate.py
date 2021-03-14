import argparse
import json
import sys
import requests
from datetime import datetime

# Go look here: https://www.dataquest.io/blog/python-api-tutorial/

def updateWallet(wallet):

    # GET all the farms info
    address = wallet["address"]
    farms = requests.get(f'https://farm.army/api/v0/farms/{address}')
    balances = requests.get(
        f'https://farm.army/api/v0/balances/{address}'
    )

    resp = {
        "wallet": wallet,
        "date": farms.headers["Date"],
        "farms": farms.json(),
        "balances": balances.json(),
    }
    # Write response
    json.dump(resp, open(wallet["datafile"],"a"))

def loadConfig(configFile):
    config = json.load(open(configFile, 'r'))
    config["wallets"] = json.load(open(config["wallet_list"]))
    return config


def dataUpdate(config):
    for wallet in config["wallets"]:
        updateWallet(wallet)


if __name__ == '__main__':
    # Create and populate argument parser
    parser = argparse.ArgumentParser(prog='dataUpdate')
    parser.add_argument('-c', '--config', type=str, nargs='?', help='Config'
                        ' json file. Default: "config.json"',
                        default='config.json')
    parser.add_argument('-v', '--verbose', type=int, nargs='?',
                        help='Different levels of debug output. Default: 0'
                        ' -1 for complete silence', default=0, const=1,
                        dest='verbose')

    # Read and convert input arguments
    args = parser.parse_args()
    config = loadConfig(args.config)
    dataUpdate(config)
